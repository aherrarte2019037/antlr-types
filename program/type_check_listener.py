from SimpleLangListener import SimpleLangListener
from SimpleLangParser import SimpleLangParser
from custom_types import IntType, FloatType, StringType, BoolType

class TypeCheckListener(SimpleLangListener):

  def __init__(self):
    self.errors = []
    self.types = {}

  def enterLogicalOp(self, ctx: SimpleLangParser.LogicalOpContext):
    pass

  def exitLogicalOp(self, ctx: SimpleLangParser.LogicalOpContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_logical_operation(left_type, right_type):
      self.errors.append(f"Logical operations (&&, ||) require boolean operands, got {left_type} and {right_type}")
    self.types[ctx] = BoolType()

  def enterComparisonOp(self, ctx: SimpleLangParser.ComparisonOpContext):
    pass

  def exitComparisonOp(self, ctx: SimpleLangParser.ComparisonOpContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_comparison_operation(left_type, right_type):
      self.errors.append(f"Comparison operations (==, !=) require compatible types, got {left_type} and {right_type}")
    self.types[ctx] = BoolType()

  def enterMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    pass

  def exitMulDiv(self, ctx: SimpleLangParser.MulDivContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_arithmetic_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for * or /: {left_type} and {right_type}")
    self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterAddSub(self, ctx: SimpleLangParser.AddSubContext):
    pass

  def exitAddSub(self, ctx: SimpleLangParser.AddSubContext):
    left_type = self.types[ctx.expr(0)]
    right_type = self.types[ctx.expr(1)]
    if not self.is_valid_add_sub_operation(left_type, right_type):
      self.errors.append(f"Unsupported operand types for + or -: {left_type} and {right_type}")
    if isinstance(left_type, StringType) and isinstance(right_type, StringType):
      self.types[ctx] = StringType()
    else:
      self.types[ctx] = FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()

  def enterInt(self, ctx: SimpleLangParser.IntContext):
    self.types[ctx] = IntType()

  def enterFloat(self, ctx: SimpleLangParser.FloatContext):
    self.types[ctx] = FloatType()

  def enterString(self, ctx: SimpleLangParser.StringContext):
    self.types[ctx] = StringType()

  def enterBool(self, ctx: SimpleLangParser.BoolContext):
    self.types[ctx] = BoolType()

  def enterParens(self, ctx: SimpleLangParser.ParensContext):
    pass

  def exitParens(self, ctx: SimpleLangParser.ParensContext):
    self.types[ctx] = self.types[ctx.expr()]

  def is_valid_arithmetic_operation(self, left_type, right_type):
    if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False

  def is_valid_add_sub_operation(self, left_type, right_type):
    # Permitir concatenación de strings
    if isinstance(left_type, StringType) and isinstance(right_type, StringType):
      return True
    elif isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False

  def is_valid_logical_operation(self, left_type, right_type):
    if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
      return True
    return False

  def is_valid_comparison_operation(self, left_type, right_type):
    # Comparaciones de igualdad permiten tipos compatibles
    if isinstance(left_type, type(right_type)):
      return True
    elif isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
      return True
    return False
