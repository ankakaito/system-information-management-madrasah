from odoo import models, fields


class SimStudent(models.Model):
    _name = "sim.student"
    _description = "Data Siswa Madrasah"
    _rec_name = "name"
    _order = "name"

    name = fields.Char(
        string="Nama Lengkap",
        required=True,
        index=True,
    )

    nis = fields.Char(
        string="NIS",
        copy=False,
        index=True,
    )

    nisn = fields.Char(
        string="NISN",
        copy=False,
        index=True,
    )

    nik = fields.Char(string="NIK")

    gender = fields.Selection(
        [
            ("male", "Laki-laki"),
            ("female", "Perempuan"),
        ],
        string="Jenis Kelamin",
    )

    birth_place = fields.Char(string="Tempat Lahir")
    birth_date = fields.Date(string="Tanggal Lahir")

    religion = fields.Selection(
        [
            ("islam", "Islam"),
            ("christian", "Kristen"),
            ("catholic", "Katolik"),
            ("hindu", "Hindu"),
            ("buddhist", "Buddha"),
            ("confucian", "Konghucu"),
            ("other", "Lainnya"),
        ],
        string="Agama",
        default="islam",
    )

    address = fields.Text(string="Alamat")
    phone = fields.Char(string="Nomor Telepon")
    email = fields.Char(string="Email")

    admission_date = fields.Date(
        string="Tanggal Masuk",
        default=fields.Date.context_today,
    )

    state = fields.Selection(
        [
            ("applicant", "Calon Siswa"),
            ("active", "Aktif"),
            ("graduated", "Lulus"),
            ("transferred", "Pindah"),
            ("inactive", "Tidak Aktif"),
        ],
        string="Status",
        default="applicant",
        required=True,
    )

    image_1920 = fields.Image(
        string="Foto Siswa",
        max_width=1920,
        max_height=1920,
    )

    guardian_link_ids = fields.One2many(
        "sim.student.guardian.link",
        "student_id",
        string="Data Wali",
    )

    education_history_ids = fields.One2many(
        "sim.student.education",
        "student_id",
        string="Riwayat Pendidikan",
    )

    notes = fields.Text(string="Catatan")

    def action_set_applicant(self):
        self.write({"state": "applicant"})
    
    def action_set_active(self):
        self.write({"state": "active"})
    
    def action_set_graduated(self):
        self.write({"state": "graduated"})
    
    def action_set_transferred(self):
        self.write({"state": "transferred"})
