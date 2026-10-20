"""Tests for tests_api.py:  venv/bin/python -m unittest test_tests_api -v"""
import collections, json, random, tempfile, unittest
from pathlib import Path

import db as user_db
user_db.DB_PATH = Path(tempfile.mkdtemp()) / "t.db"          # never touch the real users.db

from flask import Flask
from auth import auth_bp, SESSION_COOKIE
import tests_api as T

app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(T.tests_bp)
user_db.init_db()
T.init_tables()


def client(role="user", email="s@example.com", unlocks=("L1W1",)):
    uid = user_db.create_user(email, "pw-123456", role=role)
    if unlocks:
        user_db.set_unlocks(uid, list(unlocks))
    c = app.test_client()
    c.set_cookie(SESSION_COOKIE, user_db.create_session(uid))
    return c, uid


def start(c, **kw):
    r = c.post("/api/tests/start", json=kw)
    return r.status_code, r.get_json()


class Sampler(unittest.TestCase):
    banks = T.load_banks()

    def test_chapter_test_is_20_and_topic_balanced_over_many_draws(self):
        rng = random.Random(1)
        per_topic = collections.Counter()
        for _ in range(200):
            qs = T.sample_test("chapter", self.banks, rng, {}, chapter="L1W1")
            self.assertEqual(len(qs), 20)
            self.assertEqual(len({q["id"] for q in qs}), 20)
            c = collections.Counter(q["topic"] for q in qs)
            self.assertEqual(set(c.values()), {4}, c)            # 5 topics x 4
            per_topic.update(c)
        self.assertEqual(len(per_topic), 5)

    def test_every_question_eventually_appears_and_unseen_come_first(self):
        rng = random.Random(2)
        seen = {}
        for _ in range(5):                                       # 5 x 20 = whole pool of 100
            for q in T.sample_test("chapter", self.banks, rng, seen, chapter="L1W1"):
                seen[q["id"]] = seen.get(q["id"], 0) + 1
        self.assertEqual(len(seen), 100)
        self.assertEqual(max(seen.values()), 1)                  # perfect rotation: no repeat before pool is used

    def test_drill_is_one_topic(self):
        qs = T.sample_test("drill", self.banks, random.Random(3), {}, chapter="L1W1", topic="t2")
        self.assertEqual({q["topic"] for q in qs}, {"t2"})
        self.assertEqual(len(qs), 10)

    def test_hsample_spreads_across_chapters_then_topics(self):
        mk = lambda c, t, i: {"id": f"{c}{t}{i}", "chapter": c, "topic": t}
        qs = [mk(c, t, i) for c in "ab" for t in "xyz" for i in range(5)]
        tree = T.build_tree(qs, [lambda q: q["chapter"], lambda q: q["topic"]])
        out = T.hsample(12, tree, random.Random(4), {})
        self.assertEqual(collections.Counter(q["chapter"] for q in out), {"a": 6, "b": 6})
        self.assertEqual(set(collections.Counter((q["chapter"], q["topic"]) for q in out).values()), {2})

    def test_hsample_caps_by_capacity(self):
        tree = {"a": [{"id": "1"}], "b": [{"id": str(i)} for i in range(10)]}
        out = T.hsample(6, tree, random.Random(5), {})
        self.assertEqual(len(out), 6)
        self.assertEqual(sum(1 for _ in out), 6)


class Flow(unittest.TestCase):
    def test_start_hides_answers_and_explanations(self):
        c, _ = client(email="a@x.com")
        code, d = start(c, kind="chapter", chapter="L1W1")
        self.assertEqual(code, 200)
        self.assertEqual(d["total"], 20)
        blob = json.dumps(d, ensure_ascii=False)
        for forbidden in ('"correct"', '"why"', '"rule"', '"hint"'):
            self.assertNotIn(forbidden, blob)
        for it in d["items"]:
            self.assertEqual(len(it["options"]), 4)

    def test_scoring_first_try_retry_hint_and_exhaustion(self):
        c, _ = client(email="b@x.com")
        _, d = start(c, kind="chapter", chapter="L1W1")
        aid = d["attemptId"]
        bank = T.load_banks()["L1W1"]

        def correct_shown(pos):
            q = bank["q_by_id"][d["items"][pos]["id"]]
            perm = json.loads(self._perm(aid, pos))
            return perm.index(q["correct"])

        # q0: right first try -> 1.0
        r = c.post("/api/tests/answer", json={"attemptId": aid, "pos": 0, "choice": correct_shown(0)}).get_json()
        self.assertEqual((r["correct"], r["done"], r["points"]), (True, True, 1.0))
        self.assertEqual(len(r["options"]), 4)
        self.assertTrue(all(o["why"]["en"] and o["why"]["tr"] for o in r["options"]))
        self.assertEqual(sum(o["correct"] for o in r["options"]), 1)
        # answering again is refused
        self.assertEqual(c.post("/api/tests/answer", json={"attemptId": aid, "pos": 0, "choice": 0}).status_code, 409)

        # q1: wrong then right -> 0.5, wrong option's explanation shown, answer not revealed yet
        ci = correct_shown(1); wrong = (ci + 1) % 4
        r = c.post("/api/tests/answer", json={"attemptId": aid, "pos": 1, "choice": wrong}).get_json()
        self.assertEqual((r["correct"], r["done"]), (False, False))
        self.assertIn("why", r["chosen"]); self.assertNotIn("options", r); self.assertNotIn("correctIndex", r)
        self.assertEqual(c.post("/api/tests/answer", json={"attemptId": aid, "pos": 1, "choice": wrong}).status_code, 400)  # no re-pick
        r = c.post("/api/tests/answer", json={"attemptId": aid, "pos": 1, "choice": ci}).get_json()
        self.assertEqual((r["correct"], r["points"]), (True, 0.5))

        # q2: hint then right first try -> 0.75
        h = c.post("/api/tests/hint", json={"attemptId": aid, "pos": 2}).get_json()
        self.assertTrue(h["rule"]["en"] and h["rule"]["tr"])
        r = c.post("/api/tests/answer", json={"attemptId": aid, "pos": 2, "choice": correct_shown(2)}).get_json()
        self.assertEqual(r["points"], 0.75)

        # q3: three wrong -> 0 and everything revealed
        ci = correct_shown(3); wrongs = [i for i in range(4) if i != ci]
        for w in wrongs[:2]:
            r = c.post("/api/tests/answer", json={"attemptId": aid, "pos": 3, "choice": w}).get_json()
            self.assertFalse(r["done"])
        r = c.post("/api/tests/answer", json={"attemptId": aid, "pos": 3, "choice": wrongs[2]}).get_json()
        self.assertTrue(r["done"]); self.assertEqual(r["points"], 0); self.assertEqual(r["correctIndex"], ci)

        rep = c.post("/api/tests/finish", json={"attemptId": aid}).get_json()
        self.assertEqual(rep["points"], 1.0 + 0.5 + 0.75)
        self.assertEqual(rep["max"], 20.0)
        self.assertEqual(rep["hintsUsed"], 1)
        self.assertEqual(rep["retries"], 1 + 2)
        self.assertEqual(rep["masteredCount"], 1)            # only q0: first try, no hint
        self.assertEqual(rep["questions"], 20)

    def _perm(self, aid, pos):
        with user_db.db() as conn:
            return conn.execute("SELECT perm FROM tests_items WHERE attempt_id=? AND pos=?", (aid, pos)).fetchone()[0]

    def test_perfect_run_report_and_rotation_across_attempts(self):
        c, _ = client(email="c@x.com")
        bank = T.load_banks()["L1W1"]
        used = collections.Counter()
        for run in range(5):
            _, d = start(c, kind="chapter", chapter="L1W1")
            for it in d["items"]:
                used[it["id"]] += 1
                perm = json.loads(self._perm(d["attemptId"], it["pos"]))
                c.post("/api/tests/answer", json={"attemptId": d["attemptId"], "pos": it["pos"],
                                                  "choice": perm.index(bank["q_by_id"][it["id"]]["correct"])})
            rep = c.post("/api/tests/finish", json={"attemptId": d["attemptId"]}).get_json()
            self.assertEqual(rep["percent"], 100)
            self.assertEqual(rep["weak"], [])
            self.assertEqual(len(rep["history"]), run if run < 5 else 5)
        self.assertEqual(len(used), 100)                       # 5 tests covered the whole pool exactly once
        self.assertEqual(set(used.values()), {1})

    def test_weak_topics_are_reported_with_section_link(self):
        c, _ = client(email="d@x.com")
        bank = T.load_banks()["L1W1"]
        _, d = start(c, kind="chapter", chapter="L1W1")
        for it in d["items"]:
            perm = json.loads(self._perm(d["attemptId"], it["pos"]))
            ci = perm.index(bank["q_by_id"][it["id"]]["correct"])
            choice = ci if it["topic"] != "t4" else (ci + 1) % 4          # fail every t4 question first time
            c.post("/api/tests/answer", json={"attemptId": d["attemptId"], "pos": it["pos"], "choice": choice})
            if it["topic"] == "t4":
                c.post("/api/tests/answer", json={"attemptId": d["attemptId"], "pos": it["pos"], "choice": ci})
        rep = c.post("/api/tests/finish", json={"attemptId": d["attemptId"]}).get_json()
        self.assertEqual([w["topic"] for w in rep["weak"]], ["t4"])
        self.assertEqual(rep["weak"][0]["section"], 3)
        self.assertEqual((rep["weak"][0]["level"], rep["weak"][0]["week"]), (1, 1))
        self.assertEqual(rep["weak"][0]["mastery"], 0)
        self.assertEqual(len(rep["strong"]), 3)
        self.assertTrue(all(s["mastery"] == 100 for s in rep["strong"]))

    def test_locked_chapter_refused_but_admin_and_unavailable_handled(self):
        c, _ = client(email="e@x.com", unlocks=())
        self.assertEqual(start(c, kind="chapter", chapter="L1W1")[0], 403)
        self.assertEqual(start(c, kind="chapter", chapter="L9W9")[0], 404)
        self.assertEqual(start(c, kind="master")[0], 404)            # no master bank yet
        from unittest import mock                                     # level exam needs all 14 chapters of the level
        only_one = {"L1W1": T.load_banks()["L1W1"]}
        with mock.patch.object(T, "load_banks", return_value=only_one):
            self.assertEqual(start(c, kind="level", level=1)[0], 404)
        self.assertEqual(start(c, kind="nonsense")[0], 400)
        a, _ = client(role="admin", email="adm@x.com", unlocks=())
        self.assertEqual(start(a, kind="chapter", chapter="L1W1")[0], 200)

    def test_cannot_touch_someone_elses_attempt(self):
        c1, _ = client(email="f@x.com"); c2, _ = client(email="g@x.com")
        _, d = start(c1, kind="chapter", chapter="L1W1")
        self.assertEqual(c2.post("/api/tests/answer", json={"attemptId": d["attemptId"], "pos": 0, "choice": 0}).status_code, 404)
        self.assertEqual(c2.post("/api/tests/finish", json={"attemptId": d["attemptId"]}).status_code, 404)

    def test_question_report_and_catalog(self):
        c, _ = client(email="h@x.com")
        _, d = start(c, kind="chapter", chapter="L1W1")
        self.assertEqual(c.post("/api/tests/report-question", json={"qid": d["items"][0]["id"], "note": "typo?"}).status_code, 200)
        self.assertEqual(c.post("/api/tests/report-question", json={"qid": "nope", "note": "x"}).status_code, 400)
        cat = c.get("/api/tests/catalog").get_json()
        self.assertEqual(cat["chapters"]["L1W1"]["pool"], 100)
        self.assertEqual(len(cat["chapters"]["L1W1"]["topics"]), 5)

    def test_requires_login(self):
        self.assertEqual(app.test_client().post("/api/tests/start", json={"kind": "chapter"}).status_code, 401)


if __name__ == "__main__":
    unittest.main()
