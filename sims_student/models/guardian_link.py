from odoo import models, fields


class SimStudentGuardianLink(models.Model):
    _name = "sim.student.guardian.link"
    _description = "Relasi Siswa dan Wali"
    _rec_name = "guardian_id"

    student_id = fields.Many2one(
        "sim.student",
        string="Siswa",
        required=True,
        ondelete="cascade",
        index=True,
    )

    guardian_id = fields.Many2one(
        "sim.student.guardian",
        string="Wali",
        required=True,
        ondelete="restrict",
        index=True,
    )

    relationship = fields.Selection(
        [
            ("father", "Ayah"),
            ("mother", "Ibu"),
            ("legal_guardian", "Wali Sah"),
            ("other", "Lainnya"),
        ],
        string="Hubungan dengan Siswa",
        required=True,
        default="other",
    )

    is_primary = fields.Boolean(
        string="Wali Utama",
        default=False,
    )

    is_emergency_contact = fields.Boolean(
        string="Kontak Darurat",
        default=False,
    )

    lives_with_student = fields.Boolean(
        string="Tinggal Bersama Siswa",
        default=False,
    )
