from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimsPpdbPeriod(models.Model):
    _name = 'sims.ppdb.period'
    _description = 'Periode PPDB'
    _order = 'academic_year desc, wave_number asc'

    name = fields.Char(
        string='Nama Periode',
        required=True,
    )

    code = fields.Char(
        string='Kode Periode',
        required=True,
        copy=False,
    )

    academic_year = fields.Char(
        string='Tahun Ajaran',
        required=True,
        default='2027/2028',
    )

    wave_number = fields.Integer(
        string='Gelombang',
        required=True,
        default=1,
    )

    date_start = fields.Date(
        string='Tanggal Mulai Pendaftaran',
        required=True,
    )

    date_end = fields.Date(
        string='Tanggal Akhir Pendaftaran',
        required=True,
    )

    quota = fields.Integer(
        string='Kuota',
        required=True,
        default=0,
    )

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('open', 'Dibuka'),
            ('closed', 'Ditutup'),
            ('completed', 'Selesai'),
        ],
        string='Status',
        required=True,
        default='draft',
    )

    description = fields.Text(
        string='Keterangan',
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
    )

    _sql_constraints = [
        (
            'code_unique',
            'unique(code)',
            'Kode periode harus unik.'
        ),
        (
            'year_wave_unique',
            'unique(academic_year, wave_number)',
            'Nomor gelombang harus unik dalam satu tahun ajaran.'
        ),
        (
            'quota_nonnegative',
            'check(quota >= 0)',
            'Kuota tidak boleh negatif.'
        ),
        (
            'wave_positive',
            'check(wave_number > 0)',
            'Nomor gelombang harus lebih dari nol.'
        ),
    ]

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if (
                record.date_start
                and record.date_end
                and record.date_end < record.date_start
            ):
                raise ValidationError(
                    _('Tanggal akhir tidak boleh sebelum tanggal mulai.')
                )

    def action_open(self):
        for record in self:
            if record.state not in ('draft', 'closed'):
                raise ValidationError(
                    _('Hanya periode Draft atau Ditutup yang dapat dibuka.')
                )

            record.state = 'open'

    def action_close(self):
        self.write({'state': 'closed'})

    def action_complete(self):
        self.write({'state': 'completed'})

