
from odoo import models, fields, api, _


class PpdbDocumentRequirement(models.Model):
    _name = 'sims.ppdb.document.requirement'
    _description = 'Persyaratan Dokumen PPDB'
    _order = 'period_id, sequence, id'

    period_id = fields.Many2one(
        comodel_name='sims.ppdb.period',
        string='Periode PPDB',
        required=True,
        ondelete='cascade',
    )

    document_type_id = fields.Many2one(
        comodel_name='sims.ppdb.document.type',
        string='Jenis Dokumen',
        required=True,
        ondelete='restrict',
    )

    is_required = fields.Boolean(
        string='Wajib',
        default=True,
    )

    description = fields.Text(
        string='Keterangan Persyaratan',
    )

    sequence = fields.Integer(
        string='Urutan',
        default=10,
    )

    active = fields.Boolean(
        string='Aktif',
        default=True,
    )

    @api.depends('period_id.name', 'document_type_id.name')
    def _compute_display_name(self):
        for record in self:
            period = record.period_id.name or ''
            document = record.document_type_id.name or ''
    
            if period and document:
                record.display_name = f'{period} - {document}'
            elif document:
                record.display_name = document
            else:
                record.display_name = 'Persyaratan Dokumen Baru'
    
    _sql_constraints = [
        (
            'period_document_type_unique',
            'unique(period_id, document_type_id)',
            'Jenis dokumen hanya boleh ditambahkan satu kali dalam periode yang sama.',
        ),
    ]

