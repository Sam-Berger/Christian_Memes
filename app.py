import os
from flask import Flask, jsonify, abort, request
from models import setup_db, Meme, Tag
from flask_cors import CORS


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': 
            greeting = greeting + "!!!!! You are doing great in this Udacity project."
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

# MEME METHODS
    @app.route('/meme', methods=['POST'])
    def create_meme():
        body = request.get_json()
        new_title=body.get('title')
        new_url=body.get('url')
        new_tags=body.get('tags')

        # try:
        new_meme = Meme(
            title=new_title, 
            url = new_url,
            )
        for tag in new_tags:
            new_tag = Tag.query.filter_by(id=tag).first()
            new_meme.tags.append(new_tag)
        # possible need to iterate through and .append each time to get this right.
        new_meme.insert()

        return jsonify(
            {"success": True, "meme_id": new_meme.id}
        )
        # except Exception:
        #     abort(422)


    @app.route("/meme/<int:meme_id>", methods = ["DELETE"])
    def delete_meme(meme_id):
        try:
            meme = Meme.query.filter(Meme.id == meme_id).one_or_none()
            if meme is None:
                abort(404)
            meme.delete()
        
            return jsonify(
                {
                    "success": True,
                    "delete": meme_id,
                }
            )
        except:
            abort(422)

# TODO: add a new tag. need to add tags stuff in models
    @app.route("/meme/<int:meme_id>", methods = ["PATCH"])
    def update_meme(meme_id):
        print("ppp")
        body = request.get_json()
        print(body)
        new_title=body.get('title')
        new_tags=body.get('tags')

        try:
            meme = Meme.query.filter(Meme.id == meme_id).one_or_none()
            print(meme)
            if new_title is not None:
                meme.title = new_title
            if new_tags is not None:
                meme.recipe = new_tags
            meme.update()
            return jsonify(
                {
                    "success": True,
                    "memes": meme.view()
                }
            )

        except:
            abort(422)

    @app.route('/meme')
    def get_memes():
        print("hi")
        memes_query = Meme.query.all()
        if len(memes_query) == 0:
            abort(404)
        memes = []
        for meme in memes_query:
            memes.append(meme.view())
        return jsonify({
            "success": "true",
            "memes": memes
        })        


# TAG METHODS
    @app.route('/tag', methods=['POST'])
    def create_tag():
        body = request.get_json()
        new_name=body.get('name')

        try:
            new_tag = Tag(name=new_name)
            new_tag.insert()
            return jsonify(
                {"success": True, "tag_id": new_tag.id}
            )
        except Exception:
            abort(422)


    @app.route("/tag/<int:tag_id>", methods = ["DELETE"])
    def delete_tag(tag_id):
        try:
            tag = Tag.query.filter(Tag.id == tag_id).one_or_none()
            if tag is None:
                abort(404)
            tag.delete()
        
            return jsonify(
                {
                    "success": True,
                    "delete": tag_id,
                }
            )
        except:
            abort(422)


    @app.route("/tag/<int:tag_id>", methods = ["PATCH"])
    def update_tag(tag_id):
        body = request.get_json()
        new_name=body.get('name')

        try:
            tag = Tag.query.filter(Tag.id == tag_id).one_or_none()
            print(tag)
            if new_name is not None:
                tag.name = new_name
            tag.update()
            return jsonify(
                {
                    "success": True,
                    "tag": tag.view()
                }
            )

        except:
            abort(422)


    @app.route('/tag')
    def get_tags():
        tags_query = Tag.query.all()
        if len(tags_query) == 0:
            abort(404)
        tags = []
        for tag in tags_query:
            tags.append(tag.view())
        return jsonify({
            "success": "true",
            "tags": tags
        })   

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
