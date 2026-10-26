from odoo import models, fields


class SimStudentGuardian(models.Model):
    _name = "sim.student.guardian"
    _description = "Data Wali Siswa"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(
        string="Nama Lengkap",
        required=True,
        index=True,
    )

    nik = fields.Char(string="NIK")
    phone = fields.Char(string="Nomor Telepon")
    email = fields.Char(string="Email")
    occupation = fields.Char(string="Pekerjaan")
    address = fields.Text(string="Alamat")

    student_link_ids = fields.One2many(
        "sim.student.guardian.link",
        "guardian_id",
        string="Relasi Siswa",
    )
