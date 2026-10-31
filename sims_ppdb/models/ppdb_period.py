from odoo import  api, fields, models, _
from odoo.exceptions import ValidationError


class SimsPpdbPeriod(models.Model):
    _name = 'sims.ppdb.period'
    _description = 'Periode PPDB'
    _order = 'academic_year desc'

    name = fields.Char(
        string='Nama Periode',
        required=True,
    )

    code = fields.Char(
        string='Kode Periode',
        readonly=True,
        copy=False,
    )

    academic_year = fields.Char(
        string='Tahun Ajaran',
        required=True,
        default='2027/2028',
    )

    date_start = fields.Date(
        string='Tanggal Mulai Periode',
        required=True,
    )

    date_end = fields.Date(
        string='Tanggal Akhir Periode',
        required=True,
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') or vals.get('code') == 'New':
                vals['code'] = (
                    self.env['ir.sequence'].next_by_code(
                        'sims.ppdb.period'
                    ) or 'New'
                )
        return super().create(vals_list)
