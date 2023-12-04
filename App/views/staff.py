import random
import string
from flask import Blueprint, request, jsonify,url_for,redirect,render_template
from App.controllers import Student, Staff
from App.controllers.user import get_staff, get_student
from App.database import db
from flask_jwt_extended import current_user as jwt_current_user
from flask_jwt_extended import jwt_required

from App.controllers.staff import (
    search_students_searchTerm, 
    get_student_rankings,
    create_review
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')

@staff_views.route('/staff/<string:staff_id>', methods=['GET'])
def get_staff_action(staff_id):
    staff = get_staff(str(staff_id))
    if staff:
        return jsonify(staff.to_json())
    return 'Staff not found', 404

@staff_views.route('/student/<string:student_id>/reviews', methods=['POST'])
@jwt_required()
def create_review_action(student_id):
    if not jwt_current_user or not isinstance(jwt_current_user, Staff):
      return 'Unauthorized', 401

    student= get_student(str(student_id))

    if not student:
        return jsonify({"error": 'Student does not exist'}), 404

    data = request.json
    if not data['comment']:
        return "Invalid request data", 400
    
    if data['isPositive'] not in (True, False):
        return jsonify({"message": f"invalid Positivity ({data['isPositive']}). Positive: true or false"}), 400

    if not get_staff(str(jwt_current_user.ID)):
        return 'Staff does not exist', 404 

    review = create_review(jwt_current_user.ID, student_id, data['isPositive'], data['comment'])
    
    if review:
        return jsonify(review.to_json()), 201
    return 'Failed to create review', 400

@staff_views.route('/users', methods=['GET'])
def get_user_page(studentID):
    existing_student = Student.query.filter((Student.ID == studentID)).first()
    return render_template('searchStudent.html', existing_student=existing_student)

@staff_views.route('/searchStudent/search', methods=['GET'])
def search_students():
  entered = request.args.get('entered')
  if entered:
      existing_student = Student.query.filter((Student.firstname == entered) |(Student.lastname == entered) |(Student.ID == entered)).first()
      if existing_student:
          #return get_user_page(existing_student.ID)
          student_details = existing_student.to_json()
          return jsonify(student_details)
          #return render_template('searchStudent.html',student=student_details)
      else:
          return 'no_student_found'
  else:
      return "No search query entered."

@staff_views.route('/reviewlist', methods=['GET'])
def get_reviews():

  #return redirect('/')
  #if jwt_current_user and isinstance(jwt_current_user, Staff): 
  '''students = search_students_searchTerm( search_term)/<string:search_term>
  if students:
    return jsonify([student for student in students]), 200
  else:
    return jsonify({"message": f"No students found with search term {search_term}"}), 204
  #else:
    #return jsonify({"message": "You are not authorized to perform this action"}), 401'''

@staff_views.route('/rankings', methods=['GET'])
@jwt_required()
def get_karma_rankings():
  if jwt_current_user or isinstance(jwt_current_user, Staff):
    rankings = get_student_rankings(jwt_current_user) 
    if rankings:
      return jsonify(rankings), 200
    else:
      return jsonify({"message": "No rankings found"}), 204
  else:
    return jsonify({"message": "You are not authorized to perform this action"}), 401 