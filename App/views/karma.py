from flask import Blueprint, jsonify, request,render_template
from App.database import db
from App.controllers import Student,staff
from App.models import Staff

from App.controllers import *

# Create a Blueprint for karma views
karma_views = Blueprint("karma_views", __name__, template_folder='../templates')

# Route to update Karma rankings for all students

@karma_views.route('/karmaRanking/search', methods=['GET'])
def search_students_karma():
  entered = request.args.get('entered')
  if entered:
      existing_student = Student.query.filter((Student.firstname == entered) |(Student.lastname == entered) |(Student.ID == entered)).first()
      #rankings = get_student_rankings(Staff)
      if existing_student:
          #return get_user_page(existing_student.ID)
          student_details = existing_student.to_json()
          return jsonify(student_details)
          #return render_template('searchStudent.html',student=student_details)
      else:
          return 'no_student_found'
  else:
      return "No search query entered."

@karma_views.route('/karmaRanking', methods=['GET'])
def students_karma():
    rankings = get_student_rankings(Staff)
    students = get_all_students()
    return render_template('karmaRanking.html', students=rankings)

@karma_views.route("/karma/update_rankings", methods=["POST"])
def update_karma_rankings_route():
    update_student_karma_rankings()
    return "Karma rankings updated", 200
