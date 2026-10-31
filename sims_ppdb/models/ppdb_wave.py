from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimsPpdbWave(models.Model):
    _name = 'sims.ppdb.wave'
    _description = 'Gelombang Pendaftaran PPDB'
    _order = 'period_id, sequence, date_start, id'

    name = fields.Char(
        string='Nama Gelombang',
        required=True,
    )

    code = fields.Char(
        string='Kode Gelombang',
        readonly=True,
        copy=False,
    )

    period_id = fields.Many2one(
        comodel_name='sims.ppdb.period',
        string='Periode PPDB',
        required=True,
        ondelete='restrict',
    )

    date_start = fields.Date(
        string='Tanggal Mulai',
        required=True,
    )

    date_end = fields.Date(
        string='Tanggal Selesai',
        required=True,
    )

    quota = fields.Integer(
        string='Kuota Penerimaan',
        required=True,
        default=0,
    )

    sequence = fields.Integer(
        string='Urutan',
        default=10,
    )

    description = fields.Text(
        string='Keterangan',
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('open', 'Dibuka'),
            ('closed', 'Ditutup'),
        ],
        string='Status',
        default='draft',
        required=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code') or vals.get('code') == 'New':
                vals['code'] = (
                    self.env['ir.sequence'].next_by_code(
                        'sims.ppdb.wave'
                    ) or 'New'
                )

        return super().create(vals_list)

    @api.constrains('date_start', 'date_end')
    def _check_date_range(self):
        for record in self:
            if record.date_start and record.date_end:
                if record.date_end < record.date_start:
                    raise ValidationError(
                        _('Tanggal selesai tidak boleh lebih awal dari tanggal mulai.')
                    )

    @api.constrains('quota')
    def _check_quota(self):
        for record in self:
            if record.quota <= 0:
                raise ValidationError(
                    _('Kuota penerimaan tidak boleh atau kurang dari 0.')
                )

    _sql_constraints = [
        (
            'wave_code_unique',
            'unique(code)',
            'Kode gelombang harus unik.',
        ),
        (
            'wave_name_period_unique',
            'unique(name, period_id)',
            'Nama gelombang sudah digunakan pada periode PPDB ini.',
        ),
    ]
