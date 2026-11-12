
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class SimsPpdbApplicant(models.Model):
    _name = 'sims.ppdb.applicant'
    _description = 'Data Pendaftar PPDB'
    _rec_name = 'registration_number'
    _order = 'registration_date desc, id desc'

    # ---------------------------------------------------------
    # INFORMASI PENDAFTARAN
    # ---------------------------------------------------------

    registration_number = fields.Char(
        string='Nomor Pendaftaran',
        required=True,
        readonly=True,
        copy=False,
        default='New',
        index=True,
    )

    registration_date = fields.Date(
        string='Tanggal Pendaftaran',
        required=True,
        default=fields.Date.context_today,
    )

    registration_type = fields.Selection(
        selection=[
            ('online', 'Online'),
            ('offline', 'Offline'),
        ],
        string='Metode Pendaftaran',
        required=True,
        default='offline',
    )

    period_id = fields.Many2one(
        comodel_name='sims.ppdb.period',
        string='Periode PPDB',
        required=True,
        ondelete='restrict',
    )

    wave_path_id = fields.Many2one(
        comodel_name='sims.ppdb.wave.path',
        string='Gelombang dan Jalur Pendaftaran',
        required=True,
        domain="[('period_id', '=', period_id), ('active', '=', True)]",
        ondelete='restrict',
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('submitted', 'Diajukan'),
            ('verified', 'Terverifikasi'),
            ('selection', 'Dalam Seleksi'),
            ('accepted', 'Diterima'),
            ('waitlist', 'Daftar Tunggu'),
            ('rejected', 'Ditolak'),
            ('cancelled', 'Dibatalkan'),
        ],
        string='Status Pendaftaran',
        required=True,
        default='draft',
        tracking=True,
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Petugas Pendaftaran',
        default=lambda self: self.env.user,
        readonly=True,
    )

    # ---------------------------------------------------------
    # IDENTITAS CALON SISWA
    # ---------------------------------------------------------

    name = fields.Char(
        string='Nama Lengkap',
        required=True,
        index=True,
    )

    nik = fields.Char(
        string='NIK',
        size=16,
        index=True,
    )

    nisn = fields.Char(
        string='NISN',
        size=10,
        index=True,
    )

    gender = fields.Selection(
        selection=[
            ('male', 'Laki-laki'),
            ('female', 'Perempuan'),
        ],
        string='Jenis Kelamin',
    )

    birth_place = fields.Char(
        string='Tempat Lahir',
    )

    birth_date = fields.Date(
        string='Tanggal Lahir',
    )

    religion = fields.Char(
        string='Agama',
    )


    religion = fields.Selection(
        selection=[
            ('islam', 'Islam'),
            ('protestan', 'Kristen Protestan'),
            ('katolik', 'Kristen Katolik'),
            ('protestan', 'Budha'),
            ('hindu', 'Hindu'),
            ('konghucu', 'Konghucu'),
        ],
        string='Agama',
    )

    address = fields.Text(
        string='Alamat Lengkap',
    )

    phone = fields.Char(
        string='Nomor Telepon / WhatsApp',
    )

    email = fields.Char(
        string='Email',
    )

    # ---------------------------------------------------------
    # ASAL SEKOLAH
    # ---------------------------------------------------------

    school_origin = fields.Char(
        string='Asal Sekolah',
    )

    school_origin_address = fields.Char(
        string='Alamat Asal Sekolah',
    )

    school_origin_npsn = fields.Char(
        string='NPSN Asal Sekolah',
        size=8,
    )

    graduation_year = fields.Integer(
        string='Tahun Lulus',
    )

    # ---------------------------------------------------------
    # RELATION / INFORMASI TAMBAHAN
    # ---------------------------------------------------------

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Institusi',
        default=lambda self: self.env.company,
        readonly=True,
        required=True,
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
    )

    # ---------------------------------------------------------
    # CREATE
    # ---------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('registration_number') or vals.get(
                'registration_number'
            ) == 'New':
                sequence = self.env['ir.sequence'].next_by_code(
                    'sims.ppdb.applicant'
                )

                if not sequence:
                    raise UserError(
                        _('Sequence nomor pendaftaran PPDB belum dikonfigurasi.')
                    )

                vals['registration_number'] = sequence

        return super().create(vals_list)

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    @api.onchange('period_id')
    def _onchange_period_id(self):
        if self.wave_path_id and (
            self.wave_path_id.period_id != self.period_id
        ):
            self.wave_path_id = False

    @api.constrains('period_id', 'wave_path_id')
    def _check_period_wave_path(self):
        for record in self:
            if (
                record.period_id
                and record.wave_path_id
                and record.wave_path_id.period_id != record.period_id
            ):
                raise ValidationError(
                    _(
                        'Gelombang dan jalur pendaftaran harus berasal '
                        'dari periode PPDB yang dipilih.'
                    )
                )

    @api.constrains('nik')
    def _check_nik(self):
        for record in self:
            if record.nik and (
                not record.nik.isdigit() or len(record.nik) != 16
            ):
                raise ValidationError(
                    _('NIK harus terdiri dari 16 digit angka.')
                )

    @api.constrains('nisn')
    def _check_nisn(self):
        for record in self:
            if record.nisn and (
                not record.nisn.isdigit() or len(record.nisn) != 10
            ):
                raise ValidationError(
                    _('NISN harus terdiri dari 10 digit angka.')
                )

    _registration_number_unique = models.Constraint(
        'unique(registration_number)',
        'Nomor pendaftaran sudah digunakan.',
    )


    # ==========================================
    # DATA ORANG TUA / WALI
    # ==========================================

    # DATA AYAH
    father_name = fields.Char(string='Nama Ayah')
    father_nik = fields.Char(string='NIK Ayah', size=16)
    father_education = fields.Selection(
        selection=[
            ('sd', 'SD / MI'),
            ('smp', 'SMP / MTs'),
            ('sma', 'SMA / MA / SMK'),
            ('d1_d3', 'Diploma'),
            ('s1', 'S1'),
            ('s2', 'S2'),
            ('s3', 'S3'),
            ('other', 'Lainnya'),
        ],
        string='Pendidikan Terakhir Ayah',
    )
    father_occupation = fields.Char(string='Pekerjaan Ayah')
    father_income = fields.Float(string='Penghasilan Ayah per Bulan')
    father_phone = fields.Char(string='Nomor Telepon Ayah')
    father_email = fields.Char(string='Email Ayah')

    # DATA IBU
    mother_name = fields.Char(string='Nama Ibu')
    mother_nik = fields.Char(string='NIK Ibu', size=16)
    mother_education = fields.Selection(
        selection=[
            ('sd', 'SD / MI'),
            ('smp', 'SMP / MTs'),
            ('sma', 'SMA / MA / SMK'),
            ('d1_d3', 'Diploma'),
            ('s1', 'S1'),
            ('s2', 'S2'),
            ('s3', 'S3'),
            ('other', 'Lainnya'),
        ],
        string='Pendidikan Terakhir Ibu',
    )
    mother_occupation = fields.Char(string='Pekerjaan Ibu')
    mother_income = fields.Float(string='Penghasilan Ibu per Bulan')
    mother_phone = fields.Char(string='Nomor Telepon Ibu')
    mother_email = fields.Char(string='Email Ibu')

    # DATA WALI
    guardian_name = fields.Char(string='Nama Wali')
    guardian_nik = fields.Char(string='NIK Wali', size=16)
    guardian_relationship = fields.Selection(
        selection=[
            ('grandfather', 'Kakek'),
            ('grandmother', 'Nenek'),
            ('uncle', 'Paman'),
            ('aunt', 'Bibi'),
            ('sibling', 'Saudara'),
            ('other', 'Lainnya'),
        ],
        string='Hubungan dengan Calon Siswa',
    )
    guardian_education = fields.Selection(
        selection=[
            ('sd', 'SD / MI'),
            ('smp', 'SMP / MTs'),
            ('sma', 'SMA / MA / SMK'),
            ('d1_d3', 'Diploma'),
            ('s1', 'S1'),
            ('s2', 'S2'),
            ('s3', 'S3'),
            ('other', 'Lainnya'),
        ],
        string='Pendidikan Terakhir Wali',
    )
    guardian_occupation = fields.Char(string='Pekerjaan Wali')
    guardian_income = fields.Float(string='Penghasilan Wali per Bulan')
    guardian_phone = fields.Char(string='Nomor Telepon Wali')
    guardian_email = fields.Char(string='Email Wali')
    guardian_address = fields.Text(string='Alamat Wali')

