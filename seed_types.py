from app import create_app
from app.extensions import db
from app.models.verification_type import VerificationType

def seed_verification_types():
    app = create_app()
    with app.app_context():
        types = [
            ("ID Verification", "Verification of candidate's government issued ID"),
            ("Address Verification", "Verification of candidate's residential address"),
            ("Employment Verification", "Verification of candidate's previous employment history"),
            ("Education Verification", "Verification of candidate's educational qualifications"),
            ("Court Records Verification", "Checking for any criminal or civil court records"),
            ("Reference Check", "Verification of professional or personal references"),
            ("Global database Verification", "Checking global watchlists and sanction lists"),
            ("Credit Check", "Verification of candidate's credit history and score"),
            ("Social Media Verification", "Screening of candidate's public social media profiles"),
            ("Drug Test Screening", "Conducting and verifying drug test results"),
            ("Passport Verification", "Verification of candidate's passport details"),
            ("DIN Verification", "Verification of Director Identification Number")
        ]

        for name, desc in types:
            existing = VerificationType.query.filter_by(name=name).first()
            if not existing:
                new_type = VerificationType(name=name, description=desc)
                db.session.add(new_type)
                print(f"Added verification type: {name}")
            else:
                print(f"Verification type already exists: {name}")
        
        db.session.commit()
        print("Seeding completed successfully.")

if __name__ == "__main__":
    seed_verification_types()
