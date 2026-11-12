
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimsPpdbApplicantDocument(models.Model):
    _name = 'sims.ppdb.applicant.document'
    _description = 'Dokumen Persyaratan Pendaftar'
    _order = 'sequence, id'

    applicant_id = fields.Many2one(
        comodel_name='sims.ppdb.applicant',
        string='Pendaftar',
        required=True,
        ondelete='cascade',
    )

    document_requirement_id = fields.Many2one(
        comodel_name='sims.ppdb.document.requirement',
        string='Persyaratan Dokumen',
        required=True,
        ondelete='restrict',
    )

    document_type_id = fields.Many2one(
        comodel_name='sims.ppdb.document.type',
        string='Jenis Dokumen',
        related='document_requirement_id.document_type_id',
        store=True,
        readonly=True,
    )

    is_required = fields.Boolean(
        string='Wajib',
        related='document_requirement_id.is_required',
        store=True,
        readonly=True,
    )

    file = fields.Binary(
        string='File Dokumen',
        attachment=True,
    )

    filename = fields.Char(
        string='Nama File',
    )

    upload_date = fields.Date(
        string='Tanggal Upload',
        default=fields.Date.context_today,
    )

    state = fields.Selection(
        selection=[
            ('missing', 'Belum Ada'),
            ('submitted', 'Menunggu Verifikasi'),
            ('valid', 'Valid'),
            ('rejected', 'Ditolak'),
        ],
        string='Status Dokumen',
        default='missing',
        required=True,
    )

    verification_note = fields.Text(
        string='Catatan Verifikasi',
    )

    verified_by = fields.Many2one(
        comodel_name='res.users',
        string='Diverifikasi Oleh',
        readonly=True,
    )

    verification_date = fields.Datetime(
        string='Tanggal Verifikasi',
        readonly=True,
    )

    sequence = fields.Integer(
        string='Urutan',
        default=10,
    )

    @api.onchange('file')
    def _onchange_file(self):
        for record in self:
            if record.file:
                record.state = 'submitted'
                record.upload_date = fields.Date.context_today(record)

    @api.constrains('applicant_id', 'document_requirement_id')
    def _check_document_requirement(self):
        for record in self:
            if (
                record.applicant_id.wave_path_id
                and record.document_requirement_id.wave_path_id
                != record.applicant_id.wave_path_id
            ):
                raise ValidationError(
                    _(
                        'Persyaratan dokumen harus sesuai dengan '
                        'gelombang dan jalur pendaftaran Applicant.'
                    )
                )

