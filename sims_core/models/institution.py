from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimsInstitution(models.Model):
    _name = 'sims.institution'
    _description = 'Profil Sekolah / Madrasah'
    _rec_name = 'name'

    singleton_key = fields.Char(
        default='main',
        required=True,
        readonly=True,
        copy=False,
    )

    name = fields.Char(
        string='Nama Lembaga',
        required=True,
    )

    code = fields.Char(
        string='Kode Internal',
        required=True,
        copy=False,
    )

    institution_type = fields.Selection([
        ('madrasah', 'Madrasah'),
        ('general_school', 'Sekolah Umum'),
    ], string='Jenis Lembaga', required=True, default='madrasah')

    education_level = fields.Selection([
        ('ra', 'RA'),
        ('mi', 'MI'),
        ('mts', 'MTs'),
        ('ma', 'MA'),
        ('mak', 'MAK'),
        ('tk', 'TK'),
        ('sd', 'SD'),
        ('smp', 'SMP'),
        ('sma', 'SMA'),
        ('smk', 'SMK'),
        ('other', 'Lainnya'),
    ], string='Jenjang Pendidikan', required=True, default='mts')

    npsn = fields.Char(string='NPSN')
    nsm = fields.Char(string='NSM')

    accreditation = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
        ('not_accredited', 'Belum Terakreditasi'),
        ('not_applicable', 'Tidak Berlaku'),
    ], string='Akreditasi')

    address = fields.Text(string='Alamat')
    village = fields.Char(string='Desa / Kelurahan')
    district = fields.Char(string='Kecamatan')
    city = fields.Char(string='Kabupaten / Kota')
    province = fields.Char(string='Provinsi')
    postal_code = fields.Char(string='Kode Pos')

    phone = fields.Char(string='Telepon')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')

    headmaster_name = fields.Char(
        string='Nama Kepala Sekolah / Madrasah'
    )

    logo = fields.Binary(
        string='Logo',
        attachment=True,
    )

    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            'institution_singleton_unique',
            'unique(singleton_key)',
            'Database SIMS hanya dapat memiliki satu profil lembaga.'
        ),
        (
            'institution_code_unique',
            'unique(code)',
            'Kode internal lembaga harus unik.'
        ),
    ]

    @api.constrains('npsn')
    def _check_npsn(self):
        for record in self:
            if record.npsn:
                if not record.npsn.isdigit() or len(record.npsn) != 8:
                    raise ValidationError(
                        _('NPSN harus terdiri dari 8 angka.')
                    )
