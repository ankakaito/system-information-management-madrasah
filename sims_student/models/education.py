from odoo import models, fields


class SimStudentEducation(models.Model):
    _name = "sim.student.education"
    _description = "Riwayat Pendidikan Siswa"
    _order = "graduation_year desc"

    student_id = fields.Many2one(
        "sim.student",
        string="Siswa",
        required=True,
        ondelete="cascade",
        index=True,
    )

    school_name = fields.Char(
        string="Nama Sekolah Asal",
        required=True,
    )

    education_level = fields.Selection(
        [
            ("tk", "TK/RA"),
            ("sd", "SD/MI"),
            ("smp", "SMP/MTs"),
            ("sma", "SMA/MA"),
            ("other", "Lainnya"),
        ],
        string="Jenjang Pendidikan",
    )

    graduation_year = fields.Integer(
        string="Tahun Lulus",
    )

    notes = fields.Text(string="Keterangan")
