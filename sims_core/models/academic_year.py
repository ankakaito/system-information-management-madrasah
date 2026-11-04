from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SimsAcademicYear(models.Model):
    _name = 'sims.academic.year'
    _description = 'Tahun Ajaran'
    _order = 'date_start desc, id desc'

    name = fields.Char(
        string='Nama Tahun Ajaran',
        required=True,
    )

    code = fields.Char(
        string='Kode',
        required=True,
        copy=False,
        index=True,
    )

    date_start = fields.Date(
        string='Tanggal Mulai',
        required=True,
    )

    date_end = fields.Date(
        string='Tanggal Selesai',
        required=True,
    )

    semester_ids = fields.One2many(
        'sims.academic.semester',
        'academic_year_id',
        string='Semester',
    )

    semester_count = fields.Integer(
        string='Jumlah Semester',
        compute='_compute_semester_count',
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Aktif'),
        ('closed', 'Ditutup'),
    ], string='Status', default='draft', required=True)

    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            'academic_year_code_unique',
            'unique(code)',
            'Kode tahun ajaran sudah digunakan.'
        ),
    ]

    @api.depends('semester_ids')
    def _compute_semester_count(self):
        for record in self:
            record.semester_count = len(record.semester_ids)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if not record.date_start or not record.date_end:
                continue

            if record.date_start > record.date_end:
                raise ValidationError(
                    _('Tanggal mulai harus sebelum tanggal selesai.')
                )

            overlap = self.search([
                ('id', '!=', record.id),
                ('date_start', '<=', record.date_end),
                ('date_end', '>=', record.date_start),
            ], limit=1)

            if overlap:
                raise ValidationError(
                    _('Periode tahun ajaran bertumpang tindih dengan %s.')
                    % overlap.display_name
                )

    @api.constrains('state')
    def _check_single_active_year(self):
        for record in self.filtered(
            lambda rec: rec.state == 'active'
        ):
            other = self.search([
                ('id', '!=', record.id),
                ('state', '=', 'active'),
            ], limit=1)

            if other:
                raise ValidationError(
                    _('Hanya boleh ada satu tahun ajaran aktif. '
                      'Tahun ajaran aktif saat ini: %s.')
                    % other.display_name
                )

    def action_set_draft(self):
        self.write({'state': 'draft'})

    def action_set_active(self):
        self.write({'state': 'active'})

    def action_close(self):
        self.write({'state': 'closed'})
