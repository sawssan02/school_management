# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Course(models.Model):
    _name = 'school.course'
    _description = 'Cours/Matière'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nom du cours', required=True, tracking=True)
    code = fields.Char(string='Code du cours', required=True, tracking=True)
    
    # Description
    description = fields.Text(string='Description')
    syllabus = fields.Text(string='Programme')
    
    # Informations académiques
    credits = fields.Integer(string='Crédits', default=3)
    hours_per_week = fields.Integer(string='Heures par semaine', default=3)
    
    # Relations
    teacher_id = fields.Many2one('school.teacher', string='Enseignant', required=True, tracking=True)
    class_id = fields.Many2one('school.class', string='Classe', required=True, tracking=True)
    
    # Notes et présence
    grade_ids = fields.One2many('school.grade', 'course_id', string='Notes')
    schedule_ids = fields.One2many('school.schedule', 'course_id', string='Emploi du temps')
    
    # Statistiques
    average_course_grade = fields.Float(string='Moyenne du cours', compute='_compute_average_course_grade', store=True)
    total_students = fields.Integer(string="Nombre d'étudiants", related='class_id.student_count')
    
    # Dates
    start_date = fields.Date(string='Date de début')
    end_date = fields.Date(string='Date de fin')
    
    # Actif
    active = fields.Boolean(string='Actif', default=True)
    
    @api.depends('grade_ids.grade')
    def _compute_average_course_grade(self):
        for record in self:
            if record.grade_ids:
                total = sum(record.grade_ids.mapped('grade'))
                record.average_course_grade = total / len(record.grade_ids)
            else:
                record.average_course_grade = 0.0
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Le code du cours doit être unique!')
    ]
