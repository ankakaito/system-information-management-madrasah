from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimsPpdbWavePath(models.Model):
    _name = 'sims.ppdb.wave.path'
    _description = 'Jalur Pendaftaran per Gelombang'
    _order = 'wave_id, sequence, id'

    name = fields.Char(
        string='Nama Konfigurasi',
        compute='_compute_name',
        store=True,
    )

    period_id = fields.Many2one(
        comodel_name='sims.ppdb.period',
        string='Periode PPDB',
        related='wave_id.period_id',
        store=True,
        readonly=True,
    )

    wave_id = fields.Many2one(
        comodel_name='sims.ppdb.wave',
        string='Gelombang Pendaftaran',
        required=True,
        ondelete='cascade',
    )

    registration_path_id = fields.Many2one(
        comodel_name='sims.ppdb.registration.path',
        string='Jalur Pendaftaran',
        required=True,
        ondelete='restrict',
    )

    document_requirement_ids = fields.One2many(
        comodel_name='sims.ppdb.document.requirement',
        inverse_name='wave_path_id',
        string='Persyaratan Dokumen',
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

    @api.depends(
        'wave_id.name',
        'registration_path_id.name',
    )

    def _compute_name(self):
        for record in self:
            if record.wave_id and record.registration_path_id:
                record.name = '%s - %s' % (
                    record.wave_id.name,
                    record.registration_path_id.name,
                )
            else:
                record.name = 'New'

    _sql_constraints = [
        (
            'wave_registration_path_unique',
            'unique(wave_id, registration_path_id)',
            'Jalur pendaftaran tersebut sudah dikonfigurasi pada gelombang ini.',
        ),
    ]

    @api.constrains('wave_id', 'registration_path_id')
    def _check_configuration(self):
        for record in self:
            if not record.wave_id or not record.registration_path_id:
                raise ValidationError(
                    _('Gelombang dan jalur pendaftaran harus diisi.')
                )
