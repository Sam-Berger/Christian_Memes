import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Meme, Tag




class ChristianMemeTestCase(unittest.TestCase):
    """This class represents the meme test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        # self.database_path = "postgresql://{}:{}@{}/{}".format(
        #     TEST_DB_USER, TEST_DB_PASSWORD, "localhost:5432", TEST_DB_NAME)

        self.database_path = "postgresql://postgres:postgres@localhost:5432/postgres"
        self.owner = os.environ['OWNER_TOKEN']
        self.headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            },
        setup_db(self.app, self.database_path)

        self.new_meme = {
            "title": "newmeme",
            "url": "url.com",
            "tags": []
        }

        self.new_meme_422 = {
            "title": "newmeme",
            "url": "url.com",
        }

        self.new_tag = {
            "name": "newtag",
        }

        self.new_tag_422 = {}


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


# MEME TESTS

    def test_delete_meme(self):
        test_meme = Meme(title="new_title", url="new_url.com", tags = [])
        test_meme.insert()
        test_meme_id = test_meme.id

        res = self.client().delete(f'/meme/{test_meme_id}', headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            })
        data = json.loads(res.data)

        meme = Meme.query.filter(Meme.id == test_meme_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], test_meme_id)
        self.assertEqual(meme, None)

    def test_delete_meme_422(self):
        res = self.client().delete("/meme/1000000", headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_get_meme(self):
        res = self.client().get("/meme")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_meme(self):
        res = self.client().post("/meme", json=self.new_meme, 
        headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_meme_422(self):
        res = self.client().post("/meme", json=self.new_meme_422, 
        headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)


    def test_patch_meme(self):
        test_meme = Meme(title="new_title_1", url="new_url_1.com", tags = [])
        test_meme.insert()
        test_meme_id = test_meme.id
        json_patch = {"title": "edit_title"}

        res = self.client().patch(f'/meme/{test_meme_id}', 
            json=json_patch,
            headers={
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.owner}')
            }
            )
        data = json.loads(res.data)

        # meme = Meme.query.filter(Meme.id == test_meme_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['meme']['title'], json_patch["title"])

    def test_patch_meme_422(self):
        test_meme = Meme(title="new_title_1", url="new_url_1.com", tags = [])
        test_meme.insert()
        test_meme_id = test_meme.id
        json_patch = {"title": "edit_title"}

        res = self.client().patch(f'/meme/100000', 
            json=json_patch,
            headers={
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.owner}')
            }
            )
        data = json.loads(res.data)

        # meme = Meme.query.filter(Meme.id == test_meme_id).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)


# TAG TESTS

    def test_delete_tag(self):
        test_tag = Tag(name="new_name")
        test_tag.insert()
        test_tag_id = test_tag.id

        res = self.client().delete(f'/tag/{test_tag_id}', headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            })
        data = json.loads(res.data)

        tag = Tag.query.filter(Tag.id == test_tag_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], test_tag_id)
        self.assertEqual(tag, None)
        print("test")

    def test_delete_tag_422(self):
        res = self.client().delete("/tag/1000000", headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_get_tag(self):
        res = self.client().get("/tag")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_tag(self):
        res = self.client().post("/tag", json=self.new_tag, 
        headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_tag_422(self):
        res = self.client().post("/tag", json=self.new_tag_422, 
        headers={
            ('Content-Type', 'application/json'),
            ('Authorization', f'Bearer {self.owner}')
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)


    def test_patch_tag(self):
        test_tag = Tag(name="new_name_1")
        test_tag.insert()
        test_tag_id = test_tag.id
        json_patch = {"name": "edit_name"}

        res = self.client().patch(f'/tag/{test_tag_id}', 
            json=json_patch,
            headers={
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.owner}')
            }
            )
        data = json.loads(res.data)

        # tag = Tag.query.filter(Tag.id == test_tag_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['tag']['name'], json_patch["name"])

    def test_patch_tag_422(self):
        test_tag = Tag(name="new_name_1")
        test_tag.insert()
        test_tag_id = test_tag.id
        json_patch = {"name": "edit_name"}

        res = self.client().patch(f'/tag/100000', 
            json=json_patch,
            headers={
                ('Content-Type', 'application/json'),
                ('Authorization', f'Bearer {self.owner}')
            }
            )
        data = json.loads(res.data)

        # tag = Tag.query.filter(Tag.id == test_tag_id).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()