# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Attendance(models.Model):
    _name = 'school.attendance'
    _description = 'Présence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc, student_id'

    # Relations
    student_id = fields.Many2one('school.student', string='Étudiant', required=True, tracking=True)
    class_id = fields.Many2one('school.class', string='Classe', related='student_id.class_id', store=True)
    course_id = fields.Many2one('school.course', string='Cours', tracking=True)
    schedule_id = fields.Many2one('school.schedule', string='Emploi du temps', tracking=True)
    
    # Date et heure
    date = fields.Date(string='Date', default=fields.Date.today, required=True, tracking=True)
    check_in = fields.Datetime(string="Heure d'arrivée")
    check_out = fields.Datetime(string='Heure de départ')
    
    # Statut
    status = fields.Selection([
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('late', 'En retard'),
        ('excused', 'Absent justifié'),
    ], string='Statut', default='present', required=True, tracking=True)
    
    # Raison
    reason = fields.Text(string="Raison de l'absence")
    
    # Notes
    remarks = fields.Text(string='Remarques')
    
    # Marqué par
    marked_by = fields.Many2one('res.users', string='Marqué par', default=lambda self: self.env.user)
    
    # Nom affiché
    display_name = fields.Char(string='Nom', compute='_compute_display_name', store=True)
    
    @api.depends('student_id', 'date', 'status')
    def _compute_display_name(self):
        for record in self:
            status_names = dict(self._fields['status'].selection)
            status = status_names.get(record.status, '')
            student = record.student_id.name if record.student_id else ''
            date = record.date.strftime('%d/%m/%Y') if record.date else ''
            record.display_name = f"{student} - {date} - {status}"
    
    @api.constrains('check_in', 'check_out')
    def _check_times(self):
        for record in self:
            if record.check_in and record.check_out:
                if record.check_out <= record.check_in:
                    raise ValidationError(_("L'heure de départ doit être après l'heure d'arrivée."))
    
    @api.constrains('student_id', 'date', 'course_id')
    def _check_duplicate(self):
        """Empêche la duplication de présence pour le même étudiant, cours et date"""
        for record in self:
            if record.course_id:
                duplicate = self.search([
                    ('id', '!=', record.id),
                    ('student_id', '=', record.student_id.id),
                    ('date', '=', record.date),
                    ('course_id', '=', record.course_id.id),
                ])
                if duplicate:
                    raise ValidationError(_("Une présence existe déjà pour cet étudiant, ce cours et cette date."))
    
    @api.model
    def mark_bulk_attendance(self, student_ids, date, course_id, status):
        """Méthode pour marquer la présence en masse"""
        attendance_records = []
        for student_id in student_ids:
            vals = {
                'student_id': student_id,
                'date': date,
                'course_id': course_id,
                'status': status,
            }
            attendance_records.append(vals)
        return self.create(attendance_records)


class AttendanceReport(models.Model):
    _name = 'school.attendance.report'
    _description = 'Rapport de présence'
    _auto = False
    _order = 'date desc'

    student_id = fields.Many2one('school.student', string='Étudiant', readonly=True)
    class_id = fields.Many2one('school.class', string='Classe', readonly=True)
    course_id = fields.Many2one('school.course', string='Cours', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    status = fields.Selection([
        ('present', 'Présent'),
        ('absent', 'Absent'),
        ('late', 'En retard'),
        ('excused', 'Absent justifié'),
    ], string='Statut', readonly=True)
    total = fields.Integer(string='Total', readonly=True)

    def init(self):
        """Vue SQL pour les rapports de présence"""
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW school_attendance_report AS (
                SELECT
                    ROW_NUMBER() OVER (ORDER BY sa.date, sa.student_id) as id,
                    sa.student_id,
                    sa.class_id,
                    sa.course_id,
                    sa.date,
                    sa.status,
                    COUNT(*) as total
                FROM school_attendance sa
                GROUP BY sa.student_id, sa.class_id, sa.course_id, sa.date, sa.status
            )
        """)
