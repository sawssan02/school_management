# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ClassLevel(models.Model):
    _name = 'school.class'
    _description = 'Classe'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Nom de la classe', required=True, tracking=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    
    # Niveau
    level = fields.Selection([
        ('1', 'Niveau 1'),
        ('2', 'Niveau 2'),
        ('3', 'Niveau 3'),
        ('4', 'Niveau 4'),
        ('5', 'Niveau 5'),
        ('6', 'Niveau 6'),
    ], string='Niveau', required=True, tracking=True)
    
    # Section/Division
    section = fields.Char(string='Section')
    
    # Informations
    capacity = fields.Integer(string='Capacité maximale', default=30)
    room_number = fields.Char(string='Numéro de salle')
    
    # Relations
    student_ids = fields.One2many('school.student', 'class_id', string='Étudiants')
    course_ids = fields.One2many('school.course', 'class_id', string='Cours')
    schedule_ids = fields.One2many('school.schedule', 'class_id', string='Emploi du temps')
    
    # Enseignant principal
    class_teacher_id = fields.Many2one('school.teacher', string='Enseignant principal', tracking=True)
    
    # Statistiques
    student_count = fields.Integer(string="Nombre d'étudiants", compute='_compute_student_count', store=True)
    average_class_grade = fields.Float(string='Moyenne de la classe', compute='_compute_average_class_grade', store=True)
    
    # Actif
    active = fields.Boolean(string='Actif', default=True)
    
    # Notes
    notes = fields.Text(string='Notes')
    
    @api.depends('student_ids')
    def _compute_student_count(self):
        for record in self:
            record.student_count = len(record.student_ids)
    
    @api.depends('student_ids.average_grade')
    def _compute_average_class_grade(self):
        for record in self:
            if record.student_ids:
                total = sum(record.student_ids.mapped('average_grade'))
                record.average_class_grade = total / len(record.student_ids)
            else:
                record.average_class_grade = 0.0
    
    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Le code de la classe doit être unique!')
    ]
