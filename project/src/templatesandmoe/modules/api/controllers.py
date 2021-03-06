from flask import Blueprint, flash, render_template, redirect, session, jsonify
from templatesandmoe import db_session
from templatesandmoe.modules.users.service import UsersService
from templatesandmoe.modules.tags.service import TagsService


apiModule = Blueprint('api', __name__, url_prefix='/api')
users_service = UsersService(db_session)
tags = TagsService(db_session)

@apiModule.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    if session.get('user_id') and session['permission'] > 0:
        user = users_service.get_by_id(user_id)
        if user is not None:
            users_service.delete(user)
            response = jsonify({'message': 'Successfully deleted.'})

            return response
        else:
            response = jsonify({'message': 'Error with deletion.'})
            response.status_code = 500
            return response
    else:
        response = jsonify({'message': 'Access denied.'})
        response.status_code = 403
        return response


@apiModule.route('/tags/<string:tag>')
def tag_exists(tag):
    if tags.exists(tag):
        response = jsonify({'message': 'Tag exists.'})
        response.status_code = 500
        return response
    else:
        response = jsonify({'message': 'Tag does not exist'})
        response.status_code = 200
        return response