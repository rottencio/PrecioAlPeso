# main.py
# Calculadora de precio/peso con Kivy
# Versión: 0.0

# ─────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.core.image import Image as CoreImage
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

# ─────────────────────────────────────────────
# CONSTANTES GLOBALES
# ─────────────────────────────────────────────

COLOR_FONDO_APP         = get_color_from_hex("#121212")
COLOR_FONDO_TARJETA     = get_color_from_hex("#1E1E2E")
COLOR_FONDO_CABECERA    = get_color_from_hex("#181825")
COLOR_ACENTO            = get_color_from_hex("#CBA6F7")
COLOR_TEXTO_PRINCIPAL   = get_color_from_hex("#CDD6F4")
COLOR_TEXTO_SECUNDARIO  = get_color_from_hex("#A6ADC8")
COLOR_ERROR             = get_color_from_hex("#F38BA8")
COLOR_BORDE_ACTIVO      = get_color_from_hex("#CBA6F7")
COLOR_BORDE_INACTIVO    = get_color_from_hex("#313244")
COLOR_FONDO_INPUT       = get_color_from_hex("#181825")
COLOR_FONDO_SPINNER     = get_color_from_hex("#181825")

TAMANIO_FUENTE_TITULO   = dp(22)
TAMANIO_FUENTE_ETIQUETA = dp(13)
TAMANIO_FUENTE_INPUT    = dp(18)
TAMANIO_FUENTE_ERROR    = dp(11)
TAMANIO_FUENTE_SPINNER  = dp(14)

# Unidades y factores de conversión a gramos
UNIDADES_PESO = {
    "miligramos (mg)":  Decimal("0.001"),
    "gramos (g)":   Decimal("1"),
    "kilogramos (kg)":  Decimal("1000"),
    "toneladas (t)":   Decimal("1000000"),
    "granos (gr)":  Decimal("0.0648"),
    "dracmas (dr)":  Decimal("1.771845195309973"),    
    "onzas (oz)":  Decimal("28.3495"),
    "libras (lb)":  Decimal("453.592"),
    
}
UNIDADES_PESO_LISTA = list(UNIDADES_PESO.keys())

SIMBOLOS_MONEDA = ["€", "$", "£", "¥"]
SIMBOLO_DEFECTO = "€"
UNIDAD_DEFECTO  = "g"

PRECISION_CALCULO = Decimal("0.000001")
PRECISION_MOSTRAR = Decimal("0.01")


# ─────────────────────────────────────────────
# UTILIDADES PURAS
# ─────────────────────────────────────────────

def normalizar_entrada(texto: str) -> str:
    """Reemplaza coma por punto para parsear el número."""
    return texto.replace(",", ".")


def formatear_numero(valor: Decimal) -> str:
    """Formatea un Decimal a 2 decimales con coma como separador."""
    redondeado = valor.quantize(PRECISION_MOSTRAR, rounding=ROUND_HALF_UP)
    return str(redondeado).replace(".", ",")


def parsear_decimal(texto: str) -> Decimal | None:
    """
    Convierte string a Decimal.
    Acepta punto o coma como separador decimal.
    Devuelve None si no es válido o es negativo.
    """
    texto_normalizado = normalizar_entrada(texto.strip())
    if texto_normalizado in ("", "."):
        return None
    try:
        valor = Decimal(texto_normalizado)
        if valor < Decimal("0"):
            return None
        return valor
    except InvalidOperation:
        return None


def es_entrada_numerica_valida(texto: str) -> bool:
    """Valida que el texto sea numérico aceptable mientras se escribe."""
    patron = r"^\d*[.,]?\d*$"
    return bool(re.match(patron, texto))


def convertir_entre_unidades(
    valor: Decimal,
    unidad_origen: str,
    unidad_destino: str
) -> Decimal:
    """Convierte un valor de peso entre unidades pasando por gramos."""
    factor_origen  = UNIDADES_PESO[unidad_origen]
    factor_destino = UNIDADES_PESO[unidad_destino]
    valor_en_gramos = valor * factor_origen
    return (valor_en_gramos / factor_destino).quantize(
        PRECISION_CALCULO, rounding=ROUND_HALF_UP
    )


def convertir_precio_por_unidad(
    precio: Decimal,
    unidad_origen: str,
    unidad_destino: str
) -> Decimal:
    """
    Convierte el precio por unidad de peso entre unidades.
    Ejemplo: 2 €/g → 2000 €/kg
    """
    factor_origen  = UNIDADES_PESO[unidad_origen]
    factor_destino = UNIDADES_PESO[unidad_destino]
    return (precio * factor_origen / factor_destino).quantize(
        PRECISION_CALCULO, rounding=ROUND_HALF_UP
    )


def calcular_precio_total(
    precio_por_unidad: Decimal,
    peso: Decimal
) -> Decimal:
    """Calcula el precio total dado precio por unidad y peso."""
    return (precio_por_unidad * peso).quantize(
        PRECISION_CALCULO, rounding=ROUND_HALF_UP
    )


def calcular_peso(
    precio_por_unidad: Decimal,
    precio_total: Decimal
) -> Decimal | None:
    """
    Calcula el peso dado precio por unidad y precio total.
    Devuelve None si precio_por_unidad es cero.
    """
    if precio_por_unidad == Decimal("0"):
        return None
    return (precio_total / precio_por_unidad).quantize(
        PRECISION_CALCULO, rounding=ROUND_HALF_UP
    )


# ─────────────────────────────────────────────
# WIDGETS PERSONALIZADOS
# ─────────────────────────────────────────────

class TarjetaConFondo(FloatLayout):
    """
    Contenedor con fondo redondeado.
    Preparado para imagen opcional con ruta_imagen="assets/imagen.png".
    """

    def __init__(self, color_fondo=None, radio_esquinas=dp(16),
                 ruta_imagen: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.color_fondo     = color_fondo or COLOR_FONDO_TARJETA
        self.radio_esquinas  = radio_esquinas
        self._textura_imagen = None

        if ruta_imagen:
            try:
                self._textura_imagen = CoreImage(ruta_imagen).texture
            except Exception:
                self._textura_imagen = None

        self.bind(pos=self._actualizar_canvas, size=self._actualizar_canvas)

    def _actualizar_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self._textura_imagen:
                Color(1, 1, 1, 1)
                RoundedRectangle(
                    texture=self._textura_imagen,
                    pos=self.pos,
                    size=self.size,
                    radius=[self.radio_esquinas]
                )
            else:
                Color(*self.color_fondo)
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[self.radio_esquinas]
                )


class CampoNumerico(BoxLayout):
    """
    Campo de entrada numérica con etiqueta, input estilizado,
    borde dinámico y mensaje de error.
    """

    def __init__(self, etiqueta: str, en_cambio=None, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(4), **kwargs)
        self.size_hint_y = None
        self.height      = dp(90)

        self._en_cambio           = en_cambio
        self._bloqueado           = False
        self._ultimo_texto_valido = ""

        # Etiqueta
        self.lbl_etiqueta = Label(
            text=etiqueta,
            font_size=TAMANIO_FUENTE_ETIQUETA,
            color=COLOR_TEXTO_SECUNDARIO,
            size_hint_y=None,
            height=dp(18),
            halign="left",
            valign="middle",
        )
        self.lbl_etiqueta.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.add_widget(self.lbl_etiqueta)

        # Contenedor del input con borde
        self._contenedor_input = FloatLayout(
            size_hint_y=None,
            height=dp(48),
        )
        self._dibujar_borde(activo=False)

        self.entrada = TextInput(
            multiline=False,
            font_size=TAMANIO_FUENTE_INPUT,
            foreground_color=COLOR_TEXTO_PRINCIPAL,
            background_color=(0, 0, 0, 0),
            cursor_color=COLOR_ACENTO,
            hint_text="0,00",
            hint_text_color=COLOR_TEXTO_SECUNDARIO,
            padding=[dp(12), dp(10), dp(12), dp(10)],
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            input_type="number",
        )
        self.entrada.bind(text=self._al_cambiar_texto)
        self.entrada.bind(focus=self._al_cambiar_foco)
        self._contenedor_input.add_widget(self.entrada)
        self.add_widget(self._contenedor_input)

        # Mensaje de error
        self.lbl_error = Label(
            text="",
            font_size=TAMANIO_FUENTE_ERROR,
            color=COLOR_ERROR,
            size_hint_y=None,
            height=dp(16),
            halign="left",
            valign="middle",
        )
        self.lbl_error.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.add_widget(self.lbl_error)

    def _dibujar_borde(self, activo: bool):
        color = COLOR_BORDE_ACTIVO if activo else COLOR_BORDE_INACTIVO
        self._contenedor_input.canvas.before.clear()
        with self._contenedor_input.canvas.before:
            Color(*color)
            RoundedRectangle(
                pos=self._contenedor_input.pos,
                size=self._contenedor_input.size,
                radius=[dp(10)]
            )
            Color(*COLOR_FONDO_INPUT)
            RoundedRectangle(
                pos=(self._contenedor_input.x + dp(2),
                     self._contenedor_input.y + dp(2)),
                size=(self._contenedor_input.width  - dp(4),
                      self._contenedor_input.height - dp(4)),
                radius=[dp(8)]
            )
        self._contenedor_input.bind(
            pos=lambda *a: self._dibujar_borde(activo),
            size=lambda *a: self._dibujar_borde(activo),
        )

    def _al_cambiar_foco(self, instancia, tiene_foco: bool):
        self._dibujar_borde(activo=tiene_foco)

    def _al_cambiar_texto(self, instancia, nuevo_texto: str):
        if self._bloqueado:
            return

        if nuevo_texto and not es_entrada_numerica_valida(nuevo_texto):
            self._bloqueado = True
            instancia.text  = self._ultimo_texto_valido
            self._bloqueado = False
            self.mostrar_error("Solo se permiten números y un separador decimal")
            return

        self.lbl_error.text       = ""
        self._ultimo_texto_valido = nuevo_texto

        if self._en_cambio:
            self._en_cambio(nuevo_texto)

    def mostrar_error(self, mensaje: str):
        self.lbl_error.text = mensaje

    def establecer_valor(self, valor: Decimal | None):
        """Actualiza el campo programáticamente sin disparar el callback."""
        self._bloqueado = True
        if valor is None:
            self.entrada.text = ""
        else:
            self.entrada.text = formatear_numero(valor)
            self._ultimo_texto_valido = self.entrada.text
        self._bloqueado = False

    def obtener_texto(self) -> str:
        return self.entrada.text


class SelectorConEtiqueta(BoxLayout):
    """Spinner estilizado con etiqueta superior."""

    def __init__(self, etiqueta: str, opciones: list,
                 valor_defecto: str, en_cambio=None, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(4), **kwargs)
        self.size_hint_y = None
        self.height      = dp(72)
        self._en_cambio  = en_cambio

        lbl = Label(
            text=etiqueta,
            font_size=TAMANIO_FUENTE_ETIQUETA,
            color=COLOR_TEXTO_SECUNDARIO,
            size_hint_y=None,
            height=dp(18),
            halign="left",
            valign="middle",
        )
        lbl.bind(size=lambda w, s: setattr(w, "text_size", s))
        self.add_widget(lbl)

        self.spinner = Spinner(
            text=valor_defecto,
            values=opciones,
            font_size=TAMANIO_FUENTE_SPINNER,
            color=COLOR_TEXTO_PRINCIPAL,
            background_color=COLOR_FONDO_SPINNER,
            size_hint_y=None,
            height=dp(44),
        )
        self.spinner.bind(text=self._al_cambiar)
        self.add_widget(self.spinner)

    def _al_cambiar(self, instancia, valor: str):
        if self._en_cambio:
            self._en_cambio(valor)

    @property
    def valor_actual(self) -> str:
        return self.spinner.text


# ─────────────────────────────────────────────
# PANTALLA PRINCIPAL
# ─────────────────────────────────────────────

class PantallaPrincipal(BoxLayout):
    """
    Layout principal. Estructura:
    ┌─────────────────────────┐
    │  CABECERA               │ ← imagen opcional
    ├─────────────────────────┤
    │  TARJETA PRECIO/UNIDAD  │ ← imagen opcional
    │   [selector moneda]     │
    │   [selector unidad]     │
    │   [input precio/unidad] │
    ├─────────────────────────┤
    │  TARJETA PRECIO TOTAL   │ ← imagen opcional
    │   [input precio total]  │
    ├─────────────────────────┤
    │  TARJETA PESO           │ ← imagen opcional
    │   [input peso]          │
    └─────────────────────────┘
    """

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical",
                         padding=dp(16), spacing=dp(12), **kwargs)

        self._precio_por_unidad : Decimal | None = None
        self._precio_total      : Decimal | None = None
        self._peso              : Decimal | None = None
        self._unidad_actual     : str            = UNIDAD_DEFECTO
        self._simbolo_actual    : str            = SIMBOLO_DEFECTO
        self._campo_activo      : str | None     = None

        self._construir_ui()
        self._aplicar_fondo_app()

    # ── Fondo de la app ───────────────────────────────────────────────

    def _aplicar_fondo_app(self):
        """Fondo sólido de la app. Para imagen: añadir textura aquí."""
        with self.canvas.before:
            Color(*COLOR_FONDO_APP)
            self._rect_fondo = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._actualizar_fondo, size=self._actualizar_fondo)

    def _actualizar_fondo(self, *args):
        self._rect_fondo.pos  = self.pos
        self._rect_fondo.size = self.size

    # ── Construcción de la UI ─────────────────────────────────────────

    def _construir_ui(self):
        self._construir_cabecera()
        self._construir_tarjeta_precio_unidad()
        self._construir_tarjeta_precio_total()
        self._construir_tarjeta_peso()
        self.add_widget(Widget())  # Espaciador flexible

    def _construir_cabecera(self):
        """Para imagen: TarjetaConFondo(ruta_imagen='assets/logo.png')"""
        cabecera = TarjetaConFondo(
            color_fondo=COLOR_FONDO_CABECERA,
            radio_esquinas=dp(12),
            ruta_imagen=None,
            size_hint_y=None,
            height=dp(70),
        )
        titulo = Label(
            text="Calculadora Precio / Peso",
            font_size=TAMANIO_FUENTE_TITULO,
            color=COLOR_ACENTO,
            bold=True,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            halign="center",
            valign="middle",
        )
        titulo.bind(size=lambda w, s: setattr(w, "text_size", s))
        cabecera.add_widget(titulo)
        self.add_widget(cabecera)

    def _construir_tarjeta_precio_unidad(self):
        """Para imagen: TarjetaConFondo(ruta_imagen='assets/fondo_tarjeta.png')"""
        tarjeta = TarjetaConFondo(
            color_fondo=COLOR_FONDO_TARJETA,
            radio_esquinas=dp(16),
            ruta_imagen=None,
            size_hint_y=None,
            height=dp(230),
        )
        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(8),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )

        fila_selectores = BoxLayout(
            orientation="horizontal",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(72),
        )
        self.selector_moneda = SelectorConEtiqueta(
            etiqueta="Moneda",
            opciones=SIMBOLOS_MONEDA,
            valor_defecto=SIMBOLO_DEFECTO,
            en_cambio=self._al_cambiar_moneda,
            size_hint_x=0.35,
        )
        self.selector_unidad = SelectorConEtiqueta(
            etiqueta="Unidad de peso",
            opciones=UNIDADES_PESO_LISTA,
            valor_defecto=UNIDAD_DEFECTO,
            en_cambio=self._al_cambiar_unidad,
            size_hint_x=0.65,
        )
        fila_selectores.add_widget(self.selector_moneda)
        fila_selectores.add_widget(self.selector_unidad)
        contenido.add_widget(fila_selectores)

        self.campo_precio_unidad = CampoNumerico(
            etiqueta=self._etiqueta_precio_unidad(),
            en_cambio=self._al_cambiar_precio_unidad,
        )
        self.campo_precio_unidad.entrada.bind(
            focus=lambda inst, foco:
                self._registrar_campo_activo("precio_unidad", foco)
        )
        contenido.add_widget(self.campo_precio_unidad)
        tarjeta.add_widget(contenido)
        self.add_widget(tarjeta)

    def _construir_tarjeta_precio_total(self):
        """Para imagen: TarjetaConFondo(ruta_imagen='assets/fondo_precio.png')"""
        tarjeta = TarjetaConFondo(
            color_fondo=COLOR_FONDO_TARJETA,
            radio_esquinas=dp(16),
            ruta_imagen=None,
            size_hint_y=None,
            height=dp(110),
        )
        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        self.campo_precio_total = CampoNumerico(
            etiqueta=self._etiqueta_precio_total(),
            en_cambio=self._al_cambiar_precio_total,
        )
        self.campo_precio_total.entrada.bind(
            focus=lambda inst, foco:
                self._registrar_campo_activo("precio_total", foco)
        )
        contenido.add_widget(self.campo_precio_total)
        tarjeta.add_widget(contenido)
        self.add_widget(tarjeta)

    def _construir_tarjeta_peso(self):
        """Para imagen: TarjetaConFondo(ruta_imagen='assets/fondo_peso.png')"""
        tarjeta = TarjetaConFondo(
            color_fondo=COLOR_FONDO_TARJETA,
            radio_esquinas=dp(16),
            ruta_imagen=None,
            size_hint_y=None,
            height=dp(110),
        )
        contenido = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
        )
        self.campo_peso = CampoNumerico(
            etiqueta=self._etiqueta_peso(),
            en_cambio=self._al_cambiar_peso,
        )
        self.campo_peso.entrada.bind(
            focus=lambda inst, foco:
                self._registrar_campo_activo("peso", foco)
        )
        contenido.add_widget(self.campo_peso)
        tarjeta.add_widget(contenido)
        self.add_widget(tarjeta)

    # ── Etiquetas dinámicas ───────────────────────────────────────────

    def _etiqueta_precio_unidad(self) -> str:
        return f"Precio por {self._unidad_actual} ({self._simbolo_actual})"

    def _etiqueta_precio_total(self) -> str:
        return f"Precio total ({self._simbolo_actual})"

    def _etiqueta_peso(self) -> str:
        return f"Peso ({self._unidad_actual})"

    def _actualizar_etiquetas(self):
        self.campo_precio_unidad.lbl_etiqueta.text = self._etiqueta_precio_unidad()
        self.campo_precio_total.lbl_etiqueta.text  = self._etiqueta_precio_total()
        self.campo_peso.lbl_etiqueta.text          = self._etiqueta_peso()

    # ── Registro del campo activo ─────────────────────────────────────

    def _registrar_campo_activo(self, nombre_campo: str, tiene_foco: bool):
        if tiene_foco:
            self._campo_activo = nombre_campo
        elif self._campo_activo == nombre_campo:
            self._campo_activo = None

    # ── Callbacks de selectores ───────────────────────────────────────

    def _al_cambiar_moneda(self, nuevo_simbolo: str):
        self._simbolo_actual = nuevo_simbolo
        self._actualizar_etiquetas()

    def _al_cambiar_unidad(self, nueva_unidad: str):
        """
        Convierte precio/unidad y peso a la nueva unidad automáticamente.
        El precio total no cambia (es independiente de la unidad).
        """
        unidad_anterior    = self._unidad_actual
        self._unidad_actual = nueva_unidad

        if self._precio_por_unidad is not None:
            self._precio_por_unidad = convertir_precio_por_unidad(
                self._precio_por_unidad, unidad_anterior, nueva_unidad
            )
            self.campo_precio_unidad.establecer_valor(self._precio_por_unidad)

        if self._peso is not None:
            self._peso = convertir_entre_unidades(
                self._peso, unidad_anterior, nueva_unidad
            )
            self.campo_peso.establecer_valor(self._peso)

        self._actualizar_etiquetas()

    # ── Callbacks de campos de texto ──────────────────────────────────

    def _al_cambiar_precio_unidad(self, texto: str):
        self._precio_por_unidad = parsear_decimal(texto)
        self._recalcular_desde_precio_unidad()

    def _al_cambiar_precio_total(self, texto: str):
        if self._campo_activo != "precio_total":
            return
        self._precio_total = parsear_decimal(texto)
        self._recalcular_peso()

    def _al_cambiar_peso(self, texto: str):
        if self._campo_activo != "peso":
            return
        self._peso = parsear_decimal(texto)
        self._recalcular_precio_total()

    # ── Motor de cálculo ──────────────────────────────────────────────

    def _recalcular_desde_precio_unidad(self):
        """
        Al cambiar precio/unidad:
        - Si hay precio_total → recalcula peso.
        - Si hay peso         → recalcula precio_total.
        - Prioridad: precio_total sobre peso.
        """
        if self._precio_por_unidad is None:
            return
        if self._precio_total is not None:
            self._recalcular_peso()
        elif self._peso is not None:
            self._recalcular_precio_total()

    def _recalcular_precio_total(self):
        if self._precio_por_unidad is None or self._peso is None:
            return
        self._precio_total = calcular_precio_total(
            self._precio_por_unidad, self._peso
        )
        self.campo_precio_total.establecer_valor(self._precio_total)
        self.campo_precio_total.mostrar_error("")

    def _recalcular_peso(self):
        if self._precio_por_unidad is None or self._precio_total is None:
            return
        nuevo_peso = calcular_peso(self._precio_por_unidad, self._precio_total)
        if nuevo_peso is None:
            self.campo_peso.mostrar_error(
                "El precio por unidad no puede ser 0"
            )
            return
        self._peso = nuevo_peso
        self.campo_peso.establecer_valor(self._peso)
        self.campo_peso.mostrar_error("")


# ─────────────────────────────────────────────
# APLICACIÓN KIVY
# ─────────────────────────────────────────────

class CalculadoraPrecioPesoApp(App):

    def build(self):
        Window.orientation    = "portrait"
        Window.softinput_mode = "below_target"
        return PantallaPrincipal()

    def on_start(self):
        """Fuerza orientación portrait en Android."""
        try:
            from jnius import autoclass
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            ActivityInfo   = autoclass("android.content.pm.ActivityInfo")
            PythonActivity.mActivity.setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
            )
        except ImportError:
            pass


# ─────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────

if __name__ == "__main__":
    CalculadoraPrecioPesoApp().run()