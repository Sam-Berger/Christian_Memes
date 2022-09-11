import os
from flask import Flask, jsonify, abort, request
from models import setup_db, Meme, Tag
from flask_cors import CORS
from auth import AuthError, requires_auth



def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # @app.route('/')
    # def get_greeting():
    #     excited = os.environ['EXCITED']
    #     greeting = "Hello" 
    #     if excited == 'true': 
    #         greeting = greeting + "!!!!! You are doing great in this Udacity project."
    #     return greeting

    # @app.route('/coolkids')
    # def be_cool():
    #     return "Be cool, man, be coooool! You're almost a FSND grad!"

# MEME METHODS
    @app.route('/meme', methods=['POST'])
    @requires_auth('post:meme')
    def create_meme(token):
        body = request.get_json()
        new_title=body.get('title')
        new_url=body.get('url')
        new_tags=body.get('tags')
        

        try:
            new_meme = Meme(
                title=new_title, 
                url = new_url,
                )
            for tag in new_tags:
                new_tag = Tag.query.filter_by(id=tag).first()
                new_meme.tags.append(new_tag)
            new_meme.insert()

            return jsonify(
                {"success": True, "meme_id": new_meme.id}
            )
        except Exception:
            abort(422)


    @app.route("/meme/<int:meme_id>", methods = ["DELETE"])
    @requires_auth('delete:meme')
    def delete_meme(token, meme_id):
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

    @app.route("/meme/<int:meme_id>", methods = ["PATCH"])
    @requires_auth('patch:meme')
    def update_meme(token, meme_id):
        body = request.get_json()
        print(body)
        new_title=body.get('title')
        tags_to_add=body.get('tags_to_add')
        tags_to_remove=body.get('tags_to_remove')


        try:
            meme = Meme.query.filter(Meme.id == meme_id).one_or_none()
            print(meme)
            if new_title is not None:
                meme.title = new_title
            if tags_to_add is not None:
                for tag in tags_to_add:
                    new_tag = Tag.query.filter_by(id=tag).first()
                    meme.tags.append(new_tag)
            if tags_to_remove is not None:
                for tag in tags_to_remove:
                    tag_to_remove = Tag.query.filter_by(id=tag).first()
                    meme.tags.remove(tag_to_remove)
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
        memes_query = Meme.query.all()
        memes = []
        for meme in memes_query:
            memes.append(meme.view())
        return jsonify({
            "success": "true",
            "memes": memes
        })   




# TAG METHODS
    @app.route('/tag', methods=['POST'])
    @requires_auth('post:tag')
    def create_tag(token):
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
    @requires_auth('delete:tag')
    def delete_tag(token, tag_id):
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
    @requires_auth('patch:tag')
    def update_tag(token, tag_id):
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
        tags = []
        for tag in tags_query:
            tags.append(tag.view())
        return jsonify({
            "success": "true",
            "tags": tags
        })   


# Error Handlers
    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422



    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404



    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(500)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "broken"
        }), 500

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
