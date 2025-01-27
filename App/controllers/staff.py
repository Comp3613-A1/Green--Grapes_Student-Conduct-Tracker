from App.controllers.user import get_staff
from App.models import Staff, Student, Review, Karma
from App.database import db

def create_review(staffID, studentID, is_positive, comment):
    staff = get_staff(staffID)
    student = db.session.query(Student).get(studentID)
    if staff and student:
        review = staff.createReview(student,is_positive, comment)
        return review
    return None

def get_staff_reviews(staff_id):
    staff = get_staff(staff_id)
    if staff:
        return staff.getReviewsByStaff(staff)

def search_students_searchTerm(searchTerm):
    students = Staff.searchStudent(searchTerm)
    if students:
      return students
    return None
  
def get_student_rankings(staff):
    return staff.getStudentRankings()