# -*- coding: utf-8 -*-
import re

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from . import cpf


class OccMorador(models.Model):
    _name = 'occ.morador'
    _description = 'Detalhes dos Moradores'
    _order = 'name'
    _rec_name = 'name'
    _table = 'occ_morador'
    _sql_constraints = [
                        ('occ.morador', 'unique (cpf)',
                         'Já existe um morador cadastrado com este CPF!')
                       ]

    active = fields.Boolean('Ativo', default=True)
    name = fields.Char('Morador', size=45, required=True)
    image = fields.Binary('Foto')
    rg = fields.Char('RG', size=15)
    cpf = fields.Char('CPF', size=15)
    fone = fields.Char('Telefone', size=10)
    celular = fields.Char('Celular', size=11)
    veiculo_ids = fields.One2many('occ.veiculo', 'morador_id',
                                  'Veículos deste morador')
    bloco_id = fields.Many2one('occ.bloco', 'Bloco',
                               ondelete="cascade", required=True)
    apto_id = fields.Many2one('occ.apto', 'Apartamento',
                              ondelete='cascade', required=True,
                              domain="[('bloco_id','=',bloco_id)]")
    ref_ids = fields.One2many('occ.moradorref', 'morador_id',
                              'Contatos deste morador')


class OccMoradorRef(models.Model):
    _name = 'occ.moradorref'
    _description = 'Contatos de Referência dos moradores'
    _table = 'occ_moradorref'
    active = fields.Boolean('Ativo', default=True)
    name = fields.Char('Nome', size=45, required=True)
    fone = fields.Char('Telefone', size=10, required=True)
    celular = fields.Char('Celular', size=11)
    morador_id = fields.Many2one('occ.morador', 'Morador',
                                 ondelete='cascade')


@api.onchange('cpf')
def _onchange_cpf(self):
    cpf = None
    if self.cpf:
        val = re.sub('[^0-9]', '', self.cpf)
        if len(val) == 11:
            cpf = "%s.%s.%s-%s" % (
                val[0:3], val[3:6], val[6:9], val[9:11])
        self.cpf = cpf


@api.one
@api.constrains('cpf')
def _check_cpf(self):
    result = True
    if self.cpf:
        if not cpf.validate_cpf(self.cpf):
            result = False
            document = 'CPF'
    if not result:
        raise ValidationError("{} Invalido!".format(document))
