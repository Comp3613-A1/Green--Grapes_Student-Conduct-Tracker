from App.models import Review, Karma, Student,Staff
from App.database import db

def get_reviews(): 
    return db.session.query(Review).all()

def get_reviews_for_student(studentID):
    return db.session.query(Review).filter_by(studentID=studentID).all()

def get_review(reviewID):
    return Review.query.filter_by(ID=reviewID).first()

def get_reviews_by_staff(staffID):
    return db.session.query(Review).filter_by(reviewerID=staffID).all()

def create_review(reviewID, studentID, is_positive, comment):
    reviewer = Staff.query.get(reviewID)
    student = Student.query.get(studentID)
    if reviewer and student:
        new_review = Review(reviewer=reviewer, student=student, isPositive=is_positive, comment=comment)
        if is_positive:
            new_review.upvotes += 1
        else:
            new_review.downvotes += 1
        if is_positive==None:
            new_review.downvotes += 0
            new_review.upvotes += 0
        student.reviews.append(new_review)
        db.session.add(new_review)
        db.session.commit()

        return new_review 
    else:
        return None


def edit_review(review, staff, is_positive, comment):
    if review.reviewer == staff:
        review.isPositive = is_positive
        review.comment = comment
        db.session.add(review)
        db.session.commit()
        return review
    return None


def delete_review(review, staff):
    if review.reviewer == staff:
        db.session.delete(review)
        db.session.commit()
        return True
    return None


def downvoteReview(reviewID, staff):
    review = db.session.query(Review).get(reviewID)
    if staff in review.staffDownvoters:  # If they downvoted the review already, return current votes
        return review.downvotes

    else:
        if staff not in review.staffDownvoters:  # if staff has not downvoted allow the vote
            review.downvotes += 1
            review.staffDownvoters.append(staff)

            if staff in review.staffUpvoters:  # if they had upvoted previously then remove their upvote to account for switching between votes
                review.upvotes -= 1
                review.staffUpvoters.remove(staff)

        db.session.add(review)
        db.session.commit()
        # Retrieve the associated Student object using studentID
        student = db.session.query(Student).get(review.studentID)

        # Check if the student has a Karma record (karmaID) and create a new Karma record for them if not
        if student.karmaID is None:
            karma = Karma(score=0.0, rank=-99)
            db.session.add(karma)  # Add the Karma record to the session
            db.session.flush()  # Ensure the Karma record gets an ID
            db.session.commit()
            # Set the student's karmaID to the new Karma record's ID
            student.karmaID = karma.karmaID

      # Update Karma for the student
        student_karma = db.session.query(Karma).get(student.karmaID)
        student_karma.calculateScore(student)
        student_karma.updateRank()

    return review.downvotes


def upvoteReview(reviewID, staff):
    review = db.session.query(Review).get(reviewID)

    if staff in review.staffUpvoters:  # If they upvoted the review already, return current votes
        return review.upvotes

    else:
        if staff not in review.staffUpvoters:  # if staff has not upvoted allow the vote
            review.upvotes += 1
            review.staffUpvoters.append(staff)

            if staff in review.staffDownvoters:  # if they had downvoted previously then remove their downvote to account for switching between votes
                review.downvotes -= 1
                review.staffDownvoters.remove(staff)

        db.session.add(review)
        db.session.commit()
        # Retrieve the associated Student object using studentID
        student = db.session.query(Student).get(review.studentID)

        # Check if the student has a Karma record (karmaID) and create a new Karma record for them if not
        if student.karmaID is None:
            karma = Karma(score=0.0, rank=-99)
            db.session.add(karma)  # Add the Karma record to the session
            db.session.flush()  # Ensure the Karma record gets an ID
            db.session.commit()
            # Set the student's karmaID to the new Karma record's ID
            student.karmaID = karma.karmaID

      # Update Karma for the student
        student_karma = db.session.query(Karma).get(student.karmaID)
        student_karma.calculateScore(student)
        student_karma.updateRank()

    return review.upvotes

def get_all_reviews_json():
    all_reviews = db.session.query(Review).all()
    reviews_json = []

    for review in all_reviews:
        review_json = {
            "reviewID": review.ID,
            "reviewer": f"{review.reviewer.firstname} {review.reviewer.lastname}",
            "studentID": review.student.ID,
            "studentName": f"{review.student.firstname} {review.student.lastname}",
            "created": review.created.strftime("%d-%m-%Y %H:%M"),
            "isPositive": review.isPositive,
            "upvotes": review.upvotes,
            "downvotes": review.downvotes,
            "comment": review.comment
        }
        reviews_json.append(review_json)

    return reviews_json

