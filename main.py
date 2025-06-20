#Python v3.12.3
from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.lang import Builder
from kivy.base import runTouchApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.utils import platform
from kivy.properties import StringProperty
import json
from kivy.storage.jsonstore import JsonStore
import os
from kivy.uix.popup import Popup

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])

Window.clearcolor = (211/255.0, 238/255.0, 255/255.0, 0.66)

#KV-Code v2.3.0
Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        orientation: "horizontal"
        spacing: 0
        padding: 20,0,20,0

    FloatLayout:
        size_hint_x: None
        width: dp(440)
        pos_hint: {"center_x":0.5}
        padding: 20,0,20,0

        Label:
            text: "Gym-Notiz"
            font_size: dp(60)
            color: 0, 0, 0, 0.67
            size_hint: None, 1.8
            pos_hint: {"center_x":0.5}

        Image:
            source: "bg.png"
            size_hint: 1, 0.7
            pos_hint: {'x':0, 'y':0.15}
            allow_stretch: True
            keep_ratio: False

        Spinner:
            id: spinner_bizeps
            size_hint: 0.34, 0.06
            pos_hint: {'x':0.09, 'y':0.70}
            background_normal: 'transparent.png'
            background_down: 'transparent.png'
            font_size: 0
            text: ""
            values: "Bizeps-Curls (KH)", "Bizeps-Curls (LH)", "Bizepsmaschine", "Kabelzug (Bizeps)", "SZ-Curls", "Liegestütze","Klimmzüge"
            on_text:
                root.manager.current = self.text
            on_press:
                root.manager.transition.direction = "left"

        Spinner:
            id: spinner_rumpf
            size_hint: 0.43, 0.06
            pos_hint: {'x':0.27, 'y':0.65}
            background_normal: 'transparent.png'
            background_down: 'transparent.png'
            font_size: 0
            text: ""
            values: "Bankdrücken (KH)", "Bankdrücken (LH)", "Schrägbankdrücken (KH)", "Schrägbankdrücken (LH)", "Brustpresse", "Schulterpresse", "Butterfly", "Latzug"
            on_text:
                root.manager.current = self.text
            on_press:
                root.manager.transition.direction = "left"

        Spinner:
            id: spinner_trizeps
            size_hint: 0.34, 0.06
            pos_hint: {'x':0.58, 'y':0.66}
            background_normal: 'transparent.png'
            background_down: 'transparent.png'
            font_size: 0
            text: ""
            values: "Trizeps-Curls (KH)", "Trizeps-Curls (LH)", "Trizepsmaschine", "Kabelzug (Trizeps)"
            on_text:
                root.manager.current = self.text
            on_press:
                root.manager.transition.direction = "left"

        Spinner:
            id: spinner_beine
            size_hint: 0.3, 0.06
            pos_hint: {'x':0.27, 'y':0.40}
            background_normal: 'transparent.png'
            background_down: 'transparent.png'
            font_size: 0
            text: ""
            values: "Beinpresse", "Beinstrecker", "Kreuzheben", "Kniebeugen (LH)", "Laufband", "Fahrradtrainer"
            on_text:
                root.manager.current = self.text
            on_press:
                root.manager.transition.direction = "left"

    FloatLayout:
        Button:
            text: "   ...\\nMehr"
            size_hint: None, 0.2
            font_size: dp(35)
            width: 40
            height: 40
            color: 0, 0, 0, 0.67
            pos_hint: {"center_x":0.5}
            background_color: 0, 0, 0, 0
            on_press:
                root.manager.current = "mehr"
                root.manager.transition.direction = "left"

#--------------------------------------------------------

<BizepsCurlsKH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Bizeps-Curls (Kurzhanteln)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: bizeps_curls_kh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            pos_hint: {"center_x":0.5}
            input_type: 'number'
            input_filter: "float"
            multiline: False
            text: root.stored_data.get('bizeps_curls_kh')['bizeps_curls_kh_kg'] if root.stored_data.exists('bizeps_curls_kh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: bizeps_curls_kh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('bizeps_curls_kh')['bizeps_curls_kh_wiederholungen'] if root.stored_data.exists('bizeps_curls_kh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(bizeps_curls_kh_textfeld_1.text)>20 or len(bizeps_curls_kh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(bizeps_curls_kh_textfeld_1.text)>20 or len(bizeps_curls_kh_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if bizeps_curls_kh_textfeld_1.text == '' or bizeps_curls_kh_textfeld_2.text == '' or len(bizeps_curls_kh_textfeld_1.text)>20 or len(bizeps_curls_kh_textfeld_2.text)>20  else False
            on_release:
                label_gespeichert.text = "gespeichert"
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                root.stored_data.put('bizeps_curls_kh', bizeps_curls_kh_kg=bizeps_curls_kh_textfeld_1.text, bizeps_curls_kh_wiederholungen=bizeps_curls_kh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_bizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "
                label_gespeichert.color = (233/255, 14/255, 14/255, 0.8)

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<BizepsCurlsLH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Bizeps-Curls (Langhantel)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: bizeps_curls_lh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('bizeps_curls_lh')['bizeps_curls_lh_kg'] if root.stored_data.exists('bizeps_curls_lh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67

        TextInput:
            id: bizeps_curls_lh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            multiline: False
            input_type: 'number'
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('bizeps_curls_lh')['bizeps_curls_lh_wiederholungen'] if root.stored_data.exists('bizeps_curls_lh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(bizeps_curls_lh_textfeld_1.text)>20 or len(bizeps_curls_lh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(bizeps_curls_lh_textfeld_1.text)>20 or len(bizeps_curls_lh_textfeld_2.text)>20 else False

        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if bizeps_curls_lh_textfeld_1.text == '' or bizeps_curls_lh_textfeld_2.text == '' or len(bizeps_curls_lh_textfeld_1.text)>20 or len(bizeps_curls_lh_textfeld_2.text)>20  else False
            on_release:
                label_gespeichert.text = "gespeichert"
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                root.stored_data.put('bizeps_curls_lh', bizeps_curls_lh_kg=bizeps_curls_lh_textfeld_1.text, bizeps_curls_lh_wiederholungen=bizeps_curls_lh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_bizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<SZCurls>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]SZ-Curls[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: sz_curls_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            multiline: False
            pos_hint: {"center_x":0.5}
            input_type: 'number'
            input_filter: "float"
            text: root.stored_data.get('sz_curls')['sz_curls_kg'] if root.stored_data.exists('sz_curls') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: sz_curls_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            multiline: False
            input_type: 'number'
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('sz_curls')['sz_curls_wiederholungen'] if root.stored_data.exists('sz_curls') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(sz_curls_textfeld_1.text)>20 or len(sz_curls_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(sz_curls_textfeld_1.text)>20 or len(sz_curls_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67
            
        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if sz_curls_textfeld_1.text == '' or sz_curls_textfeld_2.text == '' or len(sz_curls_textfeld_1.text)>20 or len(sz_curls_textfeld_2.text)>20  else False
            on_release:
                label_gespeichert.text = "gespeichert"
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                root.stored_data.put('sz_curls', sz_curls_kg=sz_curls_textfeld_1.text, sz_curls_wiederholungen=sz_curls_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_bizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "
                label_gespeichert.color = (233/255, 14/255, 14/255, 0.8)

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<KabelzugBizeps>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Kabelzug (Bizeps)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: kabelzug_bizeps_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            multiline: False
            input_type: 'number'
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('kabelzug_bizeps')['kabelzug_bizeps_kg'] if root.stored_data.exists('kabelzug_bizeps') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: kabelzug_bizeps_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('kabelzug_bizeps')['kabelzug_bizeps_wiederholungen'] if root.stored_data.exists('kabelzug_bizeps') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(kabelzug_bizeps_textfeld_1.text)>20 or len(kabelzug_bizeps_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(kabelzug_bizeps_textfeld_1.text)>20 or len(kabelzug_bizeps_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if kabelzug_bizeps_textfeld_1.text == '' or kabelzug_bizeps_textfeld_2.text == '' or len(kabelzug_bizeps_textfeld_1.text)>20 or len(kabelzug_bizeps_textfeld_2.text)>20  else False
            on_release:
                label_gespeichert.text = "gespeichert"
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                root.stored_data.put('kabelzug_bizeps', kabelzug_bizeps_kg=kabelzug_bizeps_textfeld_1.text, kabelzug_bizeps_wiederholungen=kabelzug_bizeps_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_bizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Bizepsmaschine>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Bizepsmaschine[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: bizepsmaschine_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('bizepsmaschine')['bizepsmaschine_kg'] if root.stored_data.exists('bizepsmaschine') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: bizepsmaschine_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('bizepsmaschine')['bizepsmaschine_wiederholungen'] if root.stored_data.exists('bizepsmaschine') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(bizepsmaschine_textfeld_1.text)>20 or len(bizepsmaschine_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(bizepsmaschine_textfeld_1.text)>20 or len(bizepsmaschine_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if bizepsmaschine_textfeld_1.text == '' or bizepsmaschine_textfeld_2.text == '' or len(bizepsmaschine_textfeld_1.text)>20 or len(bizepsmaschine_textfeld_2.text)>20  else  False
            on_release:
                label_gespeichert.text = "gespeichert"
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                root.stored_data.put('bizepsmaschine', bizepsmaschine_kg=bizepsmaschine_textfeld_1.text, bizepsmaschine_wiederholungen=bizepsmaschine_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_bizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Liegestuetze>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Liegestütze[/size]\\n\\nWiederholungen"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: liegestuetze_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            pos_hint: {"center_x":0.5}
            input_type: 'number'
            multiline: False
            input_filter: "int"
            text: root.stored_data.get('liegestuetze')['liegestuetze_wiederholungen'] if root.stored_data.exists('liegestuetze') else ""

        Label:
            text: ""
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(liegestuetze_textfeld_1.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(liegestuetze_textfeld_1.text)>20 else False

        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67
            
        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if liegestuetze_textfeld_1.text == '' or len(liegestuetze_textfeld_1.text)>20 else False
            on_release:
                label_gespeichert.text = "gespeichert"
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                root.stored_data.put('liegestuetze', liegestuetze_wiederholungen=liegestuetze_textfeld_1.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_bizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "
                label_gespeichert.color = (233/255, 14/255, 14/255, 0.8)

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Klimmzuege>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Klimmzüge[/size]\\n\\nWiederholungen"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: klimmzuege_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            pos_hint: {"center_x":0.5}
            multiline: False
            input_type: 'number'
            input_filter: "int"
            text: root.stored_data.get('klimmzuege')['klimmzuege_wiederholungen'] if root.stored_data.exists('klimmzuege') else ""

        Label:
            text: ""
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(klimmzuege_textfeld_1.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(klimmzuege_textfeld_1.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67
            
        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if klimmzuege_textfeld_1.text == '' or len(klimmzuege_textfeld_1.text)>20 else False
            on_release:
                label_gespeichert.text = "gespeichert"
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                root.stored_data.put('klimmzuege', klimmzuege_wiederholungen=klimmzuege_textfeld_1.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_bizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "
                label_gespeichert.color = (233/255, 14/255, 14/255, 0.8)

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<TrizepsCurlsKH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Trizeps-Curls (Kurzhanteln)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: trizeps_curls_kh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('trizeps_curls_kh')['trizeps_curls_kh_kg'] if root.stored_data.exists('trizeps_curls_kh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: trizeps_curls_kh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            multiline: False
            input_type: 'number'
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('trizeps_curls_kh')['trizeps_curls_kh_wiederholungen'] if root.stored_data.exists('trizeps_curls_kh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(trizeps_curls_kh_textfeld_1.text)>20 or len(trizeps_curls_kh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(trizeps_curls_kh_textfeld_1.text)>20 or len(trizeps_curls_kh_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if trizeps_curls_kh_textfeld_1.text == '' or trizeps_curls_kh_textfeld_2.text == '' or len(trizeps_curls_kh_textfeld_1.text)>20 or len(trizeps_curls_kh_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.text = "gespeichert"
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                root.stored_data.put('trizeps_curls_kh', trizeps_curls_kh_kg=trizeps_curls_kh_textfeld_1.text, trizeps_curls_kh_wiederholungen=trizeps_curls_kh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_trizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<TrizepsCurlsLH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Trizeps-Curls (Langhantel)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: trizeps_curls_lh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            multiline: False
            input_type: 'number'
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('trizeps_curls_lh')['trizeps_curls_lh_kg'] if root.stored_data.exists('trizeps_curls_lh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: trizeps_curls_lh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('trizeps_curls_lh')['trizeps_curls_lh_wiederholungen'] if root.stored_data.exists('trizeps_curls_lh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(trizeps_curls_lh_textfeld_1.text)>20 or len(trizeps_curls_lh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(trizeps_curls_lh_textfeld_1.text)>20 or len(trizeps_curls_lh_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if trizeps_curls_lh_textfeld_1.text == '' or trizeps_curls_lh_textfeld_2.text == '' or len(trizeps_curls_lh_textfeld_1.text)>20 or len(trizeps_curls_lh_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('trizeps_curls_lh', trizeps_curls_lh_kg=trizeps_curls_lh_textfeld_1.text, trizeps_curls_lh_wiederholungen=trizeps_curls_lh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_trizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Trizepsmaschine>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Trizepsmaschine[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: trizepsmaschine_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            pos_hint: {"center_x":0.5}
            multiline: False
            input_filter: "float"
            text: root.stored_data.get('trizepsmaschine')['trizepsmaschine_kg'] if root.stored_data.exists('trizepsmaschine') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: trizepsmaschine_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('trizepsmaschine')['trizepsmaschine_wiederholungen'] if root.stored_data.exists('trizepsmaschine') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(trizepsmaschine_textfeld_1.text)>20 or len(trizepsmaschine_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(trizepsmaschine_textfeld_1.text)>20 or len(trizepsmaschine_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if trizepsmaschine_textfeld_1.text == '' or trizepsmaschine_textfeld_2.text == '' or len(trizepsmaschine_textfeld_1.text)>20 or len(trizepsmaschine_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('trizepsmaschine', trizepsmaschine_kg=trizepsmaschine_textfeld_1.text, trizepsmaschine_wiederholungen=trizepsmaschine_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_trizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "


        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67
#--------------------------------------------------------

<KabelzugTrizeps>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Kabelzug (Trizeps)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: kabelzug_trizeps_textfeld_1
            font_size: 60
            height: 90
            input_type: 'number'
            size_hint: 1, None
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            multiline: False
            text: root.stored_data.get('kabelzug_trizeps')['kabelzug_trizeps_kg'] if root.stored_data.exists('kabelzug_trizeps') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: kabelzug_trizeps_textfeld_2
            font_size: 60
            height: 90
            input_type: 'number'
            size_hint: 1, None
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('kabelzug_trizeps')['kabelzug_trizeps_wiederholungen'] if root.stored_data.exists('kabelzug_trizeps') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(kabelzug_trizeps_textfeld_1.text)>20 or len(kabelzug_trizeps_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(kabelzug_trizeps_textfeld_1.text)>20 or len(kabelzug_trizeps_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if kabelzug_trizeps_textfeld_1.text == '' or kabelzug_trizeps_textfeld_2.text == '' or len(kabelzug_trizeps_textfeld_1.text)>20 or len(kabelzug_trizeps_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('kabelzug_trizeps', kabelzug_trizeps_kg=kabelzug_trizeps_textfeld_1.text, kabelzug_trizeps_wiederholungen=kabelzug_trizeps_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_trizeps.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "
                
        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<BankdrueckenKH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Bankdrücken (Kurzhanteln)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: bankdruecken_kh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('bankdruecken_kh')['bankdruecken_kh_kg'] if root.stored_data.exists('bankdruecken_kh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: bankdruecken_kh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('bankdruecken_kh')['bankdruecken_kh_wiederholungen'] if root.stored_data.exists('bankdruecken_kh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(bankdruecken_kh_textfeld_1.text)>20 or len(bankdruecken_kh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(bankdruecken_kh_textfeld_1.text)>20 or len(bankdruecken_kh_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if bankdruecken_kh_textfeld_1.text == '' or bankdruecken_kh_textfeld_2.text == '' or len(bankdruecken_kh_textfeld_1.text)>20 or len(bankdruecken_kh_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('bankdruecken_kh', bankdruecken_kh_kg=bankdruecken_kh_textfeld_1.text, bankdruecken_kh_wiederholungen=bankdruecken_kh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_rumpf.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<BankdrueckenLH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Bankdrücken (Langhantel)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: bankdruecken_lh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('bankdruecken_lh')['bankdruecken_lh_kg'] if root.stored_data.exists('bankdruecken_lh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: bankdruecken_lh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('bankdruecken_lh')['bankdruecken_lh_wiederholungen'] if root.stored_data.exists('bankdruecken_lh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(bankdruecken_lh_textfeld_1.text)>20 or len(bankdruecken_lh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(bankdruecken_lh_textfeld_1.text)>20 or len(bankdruecken_lh_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if bankdruecken_lh_textfeld_1.text == '' or bankdruecken_lh_textfeld_2.text == '' or len(bankdruecken_lh_textfeld_1.text)>20 or len(bankdruecken_lh_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('bankdruecken_lh', bankdruecken_lh_kg=bankdruecken_lh_textfeld_1.text, bankdruecken_lh_wiederholungen=bankdruecken_lh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_rumpf.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<SchraegbankdrueckenKH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Schrägbankdrücken (Kurzhanteln)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: schraegbankdruecken_kh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('schraegbankdruecken_kh')['schraegbankdruecken_kh_kg'] if root.stored_data.exists('schraegbankdruecken_kh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: schraegbankdruecken_kh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('schraegbankdruecken_kh')['schraegbankdruecken_kh_wiederholungen'] if root.stored_data.exists('schraegbankdruecken_kh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(schraegbankdruecken_kh_textfeld_1.text)>20 or len(schraegbankdruecken_kh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(schraegbankdruecken_kh_textfeld_1.text)>20 or len(schraegbankdruecken_kh_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if schraegbankdruecken_kh_textfeld_1.text == '' or schraegbankdruecken_kh_textfeld_2.text == '' or len(schraegbankdruecken_kh_textfeld_1.text)>20 or len(schraegbankdruecken_kh_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('schraegbankdruecken_kh', schraegbankdruecken_kh_kg=schraegbankdruecken_kh_textfeld_1.text, schraegbankdruecken_kh_wiederholungen=schraegbankdruecken_kh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_rumpf.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<SchraegbankdrueckenLH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Schrägbankdrücken (Langhantel)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: schraegbankdruecken_lh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('schraegbankdruecken_lh')['schraegbankdruecken_lh_kg'] if root.stored_data.exists('schraegbankdruecken_lh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: schraegbankdruecken_lh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('schraegbankdruecken_lh')['schraegbankdruecken_lh_wiederholungen'] if root.stored_data.exists('schraegbankdruecken_lh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(schraegbankdruecken_lh_textfeld_1.text)>20 or len(schraegbankdruecken_lh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(schraegbankdruecken_lh_textfeld_1.text)>20 or len(schraegbankdruecken_lh_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if schraegbankdruecken_lh_textfeld_1.text == '' or schraegbankdruecken_lh_textfeld_2.text == '' or len(schraegbankdruecken_lh_textfeld_1.text)>20 or len(schraegbankdruecken_lh_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('schraegbankdruecken_lh', schraegbankdruecken_lh_kg=schraegbankdruecken_lh_textfeld_1.text, schraegbankdruecken_lh_wiederholungen=schraegbankdruecken_lh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_rumpf.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Brustpresse>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Brustpresse[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: brustpresse_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('brustpresse')['brustpresse_kg'] if root.stored_data.exists('brustpresse') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: brustpresse_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('brustpresse')['brustpresse_wiederholungen'] if root.stored_data.exists('brustpresse') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(brustpresse_textfeld_1.text)>20 or len(brustpresse_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(brustpresse_textfeld_1.text)>20 or len(brustpresse_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if brustpresse_textfeld_1.text == '' or brustpresse_textfeld_2.text == '' or len(brustpresse_textfeld_1.text)>20 or len(brustpresse_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('brustpresse', brustpresse_kg=brustpresse_textfeld_1.text, brustpresse_wiederholungen=brustpresse_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_rumpf.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Schulterpresse>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Schulterpresse[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: schulterpresse_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('schulterpresse')['schulterpresse_kg'] if root.stored_data.exists('schulterpresse') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: schulterpresse_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('schulterpresse')['schulterpresse_wiederholungen'] if root.stored_data.exists('schulterpresse') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(schulterpresse_textfeld_1.text)>20 or len(schulterpresse_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(schulterpresse_textfeld_1.text)>20 or len(schulterpresse_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if schulterpresse_textfeld_1.text == '' or schulterpresse_textfeld_2.text == '' or len(schulterpresse_textfeld_1.text)>20 or len(schulterpresse_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('schulterpresse', schulterpresse_kg=schulterpresse_textfeld_1.text, schulterpresse_wiederholungen=schulterpresse_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_rumpf.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67
            
#--------------------------------------------------------

<Butterfly>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Butterfly[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: butterfly_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('butterfly')['butterfly_kg'] if root.stored_data.exists('butterfly') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: butterfly_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('butterfly')['butterfly_wiederholungen'] if root.stored_data.exists('butterfly') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(butterfly_textfeld_1.text)>20 or len(butterfly_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(butterfly_textfeld_1.text)>20 or len(butterfly_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if butterfly_textfeld_1.text == '' or butterfly_textfeld_2.text == '' or len(butterfly_textfeld_1.text)>20 or len(butterfly_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('butterfly', butterfly_kg=butterfly_textfeld_1.text, butterfly_wiederholungen=butterfly_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_rumpf.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Latzug>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Latzug[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: latzug_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('latzug')['latzug_kg'] if root.stored_data.exists('latzug') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: latzug_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('latzug')['latzug_wiederholungen'] if root.stored_data.exists('latzug') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(latzug_textfeld_1.text)>20 or len(latzug_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(latzug_textfeld_1.text)>20 or len(latzug_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if latzug_textfeld_1.text == '' or latzug_textfeld_2.text == '' or len(latzug_textfeld_1.text)>20 or len(latzug_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('latzug', latzug_kg=latzug_textfeld_1.text, latzug_wiederholungen=latzug_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_rumpf.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Beinpresse>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Beinpresse[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: beinpresse_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('beinpresse')['beinpresse_kg'] if root.stored_data.exists('beinpresse') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: beinpresse_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('beinpresse')['beinpresse_wiederholungen'] if root.stored_data.exists('beinpresse') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(beinpresse_textfeld_1.text)>20 or len(beinpresse_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(beinpresse_textfeld_1.text)>20 or len(beinpresse_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if beinpresse_textfeld_1.text == '' or beinpresse_textfeld_2.text == '' or len(beinpresse_textfeld_1.text)>20 or len(beinpresse_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('beinpresse', beinpresse_kg=beinpresse_textfeld_1.text, beinpresse_wiederholungen=beinpresse_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_beine.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Beinstrecker>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Beinstrecker[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: beinstrecker_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('beinstrecker')['beinstrecker_kg'] if root.stored_data.exists('beinstrecker') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: beinstrecker_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('beinstrecker')['beinstrecker_wiederholungen'] if root.stored_data.exists('beinstrecker') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(beinstrecker_textfeld_1.text)>20 or len(beinstrecker_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(beinstrecker_textfeld_1.text)>20 or len(beinstrecker_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if beinstrecker_textfeld_1.text == '' or beinstrecker_textfeld_2.text == '' or len(beinstrecker_textfeld_1.text)>20 or len(beinstrecker_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('beinstrecker', beinstrecker_kg=beinstrecker_textfeld_1.text, beinstrecker_wiederholungen=beinstrecker_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_beine.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

<Kreuzheben>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Kreuzheben[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: kreuzheben_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('kreuzheben')['kreuzheben_kg'] if root.stored_data.exists('kreuzheben') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: kreuzheben_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('kreuzheben')['kreuzheben_wiederholungen'] if root.stored_data.exists('kreuzheben') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(kreuzheben_textfeld_1.text)>20 or len(kreuzheben_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(kreuzheben_textfeld_1.text)>20 or len(kreuzheben_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if kreuzheben_textfeld_1.text == '' or kreuzheben_textfeld_2.text == '' or len(kreuzheben_textfeld_1.text)>20 or len(kreuzheben_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('kreuzheben', kreuzheben_kg=kreuzheben_textfeld_1.text, kreuzheben_wiederholungen=kreuzheben_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_beine.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<KniebeugenKH>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Kniebeugen (Langhantel)[/size]\\n\\nKilo / LBS"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: kniebeugen_lh_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('kniebeugen_lh')['kniebeugen_lh_kg'] if root.stored_data.exists('kniebeugen_lh') else ""

        Label:
            text: "Wiederholungen"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
 
        TextInput:
            id: kniebeugen_lh_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('kniebeugen_lh')['kniebeugen_lh_wiederholungen'] if root.stored_data.exists('kniebeugen_lh') else ""
            input_filter: "int"

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(kniebeugen_lh_textfeld_1.text)>20 or len(kniebeugen_lh_textfeld_2.text)>20 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(kniebeugen_lh_textfeld_1.text)>20 or len(kniebeugen_lh_textfeld_2.text)>20 else False
            
        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if kniebeugen_lh_textfeld_1.text == '' or kniebeugen_lh_textfeld_2.text == '' or len(kniebeugen_lh_textfeld_1.text)>20 or len(kniebeugen_lh_textfeld_2.text)>20 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('kniebeugen_lh', kniebeugen_lh_kg=kniebeugen_lh_textfeld_1.text, kniebeugen_lh_wiederholungen=kniebeugen_lh_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_beine.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Laufband>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Laufband[/size]\\n\\nKilometer / Mile"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: laufband_textfeld_1
            font_size: 60
            height: 90
            input_type: 'number'
            multiline: False
            size_hint: 1, None
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('laufband')['laufband_kg'] if root.stored_data.exists('laufband') else ""

        Label:
            text: "Zeit (Stunden : Minuten : Sekunden)"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67
            
        TextInput:
            id: laufband_textfeld_2
            font_size: 60
            height: 90
            size_hint: 1, None
            multiline: False
            pos_hint: {"center_x":0.5}
            text: root.stored_data.get('laufband')['laufband_wiederholungen'] if root.stored_data.exists('laufband') else ""    
            
        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(laufband_textfeld_1.text)>15 or len(laufband_textfeld_2.text)>15 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(laufband_textfeld_1.text)>20 or len(laufband_textfeld_2.text)>20 else False

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if laufband_textfeld_1.text == '' or laufband_textfeld_2.text == '' or len(laufband_textfeld_1.text)>15 or len(laufband_textfeld_2.text)>15 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('laufband', laufband_kg=laufband_textfeld_1.text, laufband_wiederholungen=laufband_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_beine.text = "Trainingsgerät auswählen"
                label_gespeichert.text = " "

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<Fahrradtrainer>:
    BoxLayout:
        orientation: "vertical"
        padding: 40,0,40,20

        Label:
            text: ""
            size_hint_y: 2
            font_size: 18
            color: 0, 0, 0, 0.67

        Label:
            markup: True
            text: "[size=80]Fahrradtrainer[/size]\\n\\nKilometer / Mile"
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 60
            color: 0, 0, 0, 0.67

        TextInput:
            id: fahrradtrainer_textfeld_1
            font_size: 60
            height: 90
            size_hint: 1, None
            input_type: 'number'
            multiline: False
            pos_hint: {"center_x":0.5}
            input_filter: "float"
            text: root.stored_data.get('fahrradtrainer')['fahrradtrainer_kg'] if root.stored_data.exists('fahrradtrainer') else ""

        Label:
            text: "Zeit (Stunden : Minuten : Sekunden)"
            padding: 0, 20, 0, 0
            font_size: 60
            size_hint: 1, None
            text_size: self.width, None
            height: self.texture_size[1]
            color: 0, 0, 0, 0.67

        TextInput:
            id: fahrradtrainer_textfeld_2
            font_size: 60
            height: 90
            multiline: False
            size_hint: 1, None
            text: root.stored_data.get('fahrradtrainer')['fahrradtrainer_wiederholungen'] if root.stored_data.exists('fahrradtrainer') else ""

        Label:
            id: label_gespeichert
            text: "zu viele Zeichen!" if len(fahrradtrainer_textfeld_1.text)>15 or len(fahrradtrainer_textfeld_2.text)>15 else " "
            size_hint: 1.5, None
            text_size: self.width, None
            height: self.texture_size[1]
            font_size: 55
            color: 233/255, 14/255, 14/255, 0.8 if len(fahrradtrainer_textfeld_1.text)>20 or len(fahrradtrainer_textfeld_2.text)>20 else False

        Label:
            text: ""
            size_hint_y: 0.2
            font_size: 18
            color: 0, 0, 0, 0.67

        Button:
            id: button_speichern
            text: "Speichern"
            pos_hint: {"center_x":0.5}
            size_hint: 0, None
            font_size: 60
            width: 320
            height: 90
            disabled: True if fahrradtrainer_textfeld_1.text == "" or fahrradtrainer_textfeld_2.text == "" or len(fahrradtrainer_textfeld_1.text)>15 or len(fahrradtrainer_textfeld_2.text)>15 else False
            on_release:
                label_gespeichert.color = (40/255, 112/255, 34/255, 0.8)
                label_gespeichert.text = "gespeichert"
                root.stored_data.put('fahrradtrainer', fahrradtrainer_kg=fahrradtrainer_textfeld_1.text, fahrradtrainer_wiederholungen=fahrradtrainer_textfeld_2.text)

        Button:
            text: "< Zurück"
            size_hint: 0.3, None
            font_size: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_release:
                root.manager.transition.direction = "right"
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.get_screen("Trainingsgerät auswählen").ids.spinner_beine.text = "Trainingsgerät auswählen"

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

#--------------------------------------------------------

<mehr>:
    BoxLayout:
        orientation: "vertical"
        spacing: 10
        padding: 20

        Label:
            text: ""
            size_hint_y: 25
            font_size: dp(18)
            color: 0, 0, 0, 0.67

        ScrollView:
            size_hint: 1, 200
            do_scroll_x: False
            do_scroll_y: True
            bar_width: dp(5)
            bar_color: [0, 0, 0, 0.67]
            bar_inactive_color: [0, 0, 0, 0.67]
            
            Label:
                markup: True
                text: "[b][size=80]Was ist Gym-Notiz?[/size][/b]\\n\\nMit Gym-Notiz kann man schnell und einfach das Rekordgewicht von verschiedenen Fitnessübungen speichern und abrufen.\\nEinfach auf einen roten Punkt tippen und eine Fitnessübung auswählen."
                size_hint_y: None
                height: self.texture_size[1]
                text_size: self.width, None
                padding: 20, 0, 40, 0
                font_size: dp(30)
                color: 0, 0, 0, 0.67
 
        Button:
            id: button_clear
            text: "Alle Daten löschen"
            pos_hint: {"center_x":0.5}
            size_hint: None, None
            width:360
            height: 40
            font_size: dp(25)
            background_color: 0, 0, 0, 0
            color: 233/255, 14/255, 14/255, 0.8
            on_release:
                root.popup_fenster()
        Label:
            text: ""
            size_hint_y: 20
            font_size: 18
            color: 0, 0, 0, 0.67

        ScrollView:
            size_hint: 1, None
            height: 200
            do_scroll_x: False
            do_scroll_y: False

            Label:
                text: "Version 1.0\\nDeveloped by P A G O O K"
                padding: 0, 0, 30, 0
                height: self.texture_size[1]
                text_size: self.size
                halign: 'right'
                font_size: dp(24)
                color: 0, 0, 0, 0.67
                
        Label:
            text: ""
            size_hint_y: 12
            font_size: 18
            color: 0, 0, 0, 0.67
            
        Button:
            text: "< Zurück"
            size_hint: 0.4, None
            size_hint_y: 0
            font_size: 60
            width: 130
            height: 60
            background_color: 0, 0, 0, 0
            color: 0, 0, 0, 0.67
            on_press:
                root.manager.current = "Trainingsgerät auswählen"
                root.manager.transition.direction = "right"

        Label:
            text: ""
            size_hint_y: 15
            font_size: 18
            color: 0, 0, 0, 0.67

<PopupFenster>:
    BoxLayout:
        orientation: "vertical"
        spacing: 15
        padding: 20, 0, 20, 0

        Label:
            id: popup_label
            text: "Alle Daten löschen?"
            font_size: dp(25)

        Button:
            id: button_ja
            text: "Ja"
            height: 70
            font_size: dp(20)
            on_release:
                root.alle_daten_loeschen()
                popup_label.text="\\nAlle Daten wurden gelöscht.\\nBitte die App neu starten."
                button_ja.text=""
                button_ja.background_color= 0, 0, 0, 0
                button_nein.text="Schließen"

        Button:
            id: button_nein
            text: "Nein"
            width: 200
            font_size: dp(20)            
            height: 70
            on_release:
                root.dismiss()
""")

class PopupFenster(Popup):
            def alle_daten_loeschen(self):
                if os.path.exists("bizeps_curls_kh.json"): os.remove("bizeps_curls_kh.json")
                if os.path.exists("bizeps_curls_lh.json"): os.remove("bizeps_curls_lh.json")
                if os.path.exists("sz_curls.json"): os.remove("sz_curls.json")
                if os.path.exists("trizeps_curls_kh.json"): os.remove("trizeps_curls_kh.json")
                if os.path.exists("trizeps_curls_lh.json"): os.remove("trizeps_curls_lh.json")
                if os.path.exists("trizepsmaschine.json"): os.remove("trizepsmaschine.json")
                if os.path.exists("kabelzug_trizeps.json"): os.remove("kabelzug_trizeps.json")
                if os.path.exists("bankdruecken_kh.json"): os.remove("bankdruecken_kh.json")
                if os.path.exists("bankdruecken_lh.json"): os.remove("bankdruecken_lh.json")
                if os.path.exists("kabelzug_bizeps.json"): os.remove("kabelzug_bizeps.json")
                if os.path.exists("schraegbankdruecken_lh.json"): os.remove("schraegbankdruecken_lh.json")
                if os.path.exists("schraegbankdruecken_kh.json"): os.remove("schraegbankdruecken_kh.json")
                if os.path.exists("bizepsmaschine.json"): os.remove("bizepsmaschine.json")
                if os.path.exists("liegestuetze.json"): os.remove("liegestuetze.json")
                if os.path.exists("klimmzuege.json"): os.remove("klimmzuege.json")
                if os.path.exists("brustpresse.json"): os.remove("brustpresse.json")
                if os.path.exists("schulterpresse.json"): os.remove("schulterpresse.json")                
                if os.path.exists("beinpresse.json"): os.remove("beinpresse.json")
                if os.path.exists("beinstrecker.json"): os.remove("beinstrecker.json")
                if os.path.exists("kreuzheben.json"): os.remove("kreuzheben.json")
                if os.path.exists("kniebeugen_lh.json"): os.remove("kniebeugen_lh.json")
                if os.path.exists("laufband.json"): os.remove("laufband.json")
                if os.path.exists("fahrradtrainer.json"): os.remove("fahrradtrainer.json")
                if os.path.exists("butterfly.json"): os.remove("butterfly.json")
                if os.path.exists("latzug.json"): os.remove("latzug.json")
                else:
                    None
            pass

class GymNotizApp(App):

    def build(self):
        self.icon = r'icon.png'
        layout_vertical = BoxLayout(orientation="vertical", spacing=10, padding=20)

        class MenuScreen(Screen):
            pass

        class BizepsCurlsKH(Screen):
            stored_data = JsonStore("bizeps_curls_kh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("bizeps_curls_kh.json")
    
        class BizepsCurlsLH(Screen):
            stored_data = JsonStore("bizeps_curls_lh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("bizeps_curls_lh.json")

        class SZCurls(Screen):
            stored_data = JsonStore("sz_curls.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("sz_curls.json")

        class Liegestuetze(Screen):
            stored_data = JsonStore("liegestuetze.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("liegestuetze.json")

        class Klimmzuege(Screen):
            stored_data = JsonStore("klimmzuege.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("klimmzuege.json")

        class TrizepsCurlsKH(Screen):
            stored_data = JsonStore("trizeps_curls_kh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("trizeps_curls_kh.json")

        class TrizepsCurlsLH(Screen):
            stored_data = JsonStore("trizeps_curls_lh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("trizeps_curls_lh.json")

        class Trizepsmaschine(Screen):
            stored_data = JsonStore("trizepsmaschine.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("trizepsmaschine.json")

        class KabelzugTrizeps(Screen):
            stored_data = JsonStore("kabelzug_trizeps.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("kabelzug_trizeps.json")

        class BankdrueckenKH(Screen):
            stored_data = JsonStore("bankdruecken_kh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("bankdruecken_kh.json")

        class BankdrueckenLH(Screen):
            stored_data = JsonStore("bankdruecken_lh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("bankdruecken_lh.json")

        class SchraegbankdrueckenKH(Screen):
            stored_data = JsonStore("schraegbankdruecken_kh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("schraegbankdruecken_kh.json")

        class SchraegbankdrueckenLH(Screen):
            stored_data = JsonStore("schraegbankdruecken_lh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("schraegbankdruecken_lh.json")

        class KabelzugBizeps(Screen):
            stored_data = JsonStore("kabelzug_bizeps.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("kabelzug_bizeps.json")

        class Schrägbankdrücken(Screen):
            stored_data = JsonStore("schraegbankdruecken.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("schraegbankdruecken.json")
            
        class Bizepsmaschine(Screen):
            stored_data = JsonStore("bizepsmaschine.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("bizepsmaschine.json")

        class Brustpresse(Screen):
            stored_data = JsonStore("brustpresse.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("brustpresse.json")
            
        class Schulterpresse(Screen):
            stored_data = JsonStore("schulterpresse.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("schulterpresse.json")            
            
        class Latzug(Screen):
            stored_data = JsonStore("latzug.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("latzug.json")
            
        class Beinpresse(Screen):
            stored_data = JsonStore("beinpresse.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("beinpresse.json")

        class Beinstrecker(Screen):
            stored_data = JsonStore("beinstrecker.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("beinstrecker.json")

        class Kreuzheben(Screen):
            stored_data = JsonStore("kreuzheben.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("kreuzheben.json")

        class KniebeugenKH(Screen):
            stored_data = JsonStore("kniebeugen_lh.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("kniebeugen_lh.json")

        class Laufband(Screen):
            stored_data = JsonStore("laufband.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("laufband.json")

        class Fahrradtrainer(Screen):
            stored_data = JsonStore("fahrradtrainer.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("fahrradtrainer.json")

        class Butterfly(Screen):
            stored_data = JsonStore("butterfly.json")
        def __init__(self, *args, **kwargs):
            super(BoxLayout, self).__init__(*args, **kwargs)
            self.stored_data = JsonStore("butterfly.json")

        class mehr(Screen):
            def popup_fenster(self):
                popupfenster = PopupFenster(title="", separator_height="0", size_hint=(None,None), size=(700,380))
                popupfenster.open()
                pass
            pass

        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="Trainingsgerät auswählen"))
        sm.add_widget(BizepsCurlsKH(name="Bizeps-Curls (KH)"))
        sm.add_widget(BizepsCurlsLH(name="Bizeps-Curls (LH)"))
        sm.add_widget(SZCurls(name="SZ-Curls"))
        sm.add_widget(Bizepsmaschine(name="Bizepsmaschine"))
        sm.add_widget(KabelzugBizeps(name="Kabelzug (Bizeps)"))
        sm.add_widget(Liegestuetze(name="Liegestütze"))
        sm.add_widget(Klimmzuege(name="Klimmzüge"))
        sm.add_widget(TrizepsCurlsKH(name="Trizeps-Curls (KH)"))
        sm.add_widget(TrizepsCurlsLH(name="Trizeps-Curls (LH)"))
        sm.add_widget(Trizepsmaschine(name="Trizepsmaschine"))
        sm.add_widget(KabelzugTrizeps(name="Kabelzug (Trizeps)"))
        sm.add_widget(BankdrueckenKH(name="Bankdrücken (KH)"))
        sm.add_widget(BankdrueckenLH(name="Bankdrücken (LH)"))
        sm.add_widget(SchraegbankdrueckenKH(name="Schrägbankdrücken (KH)"))
        sm.add_widget(SchraegbankdrueckenLH(name="Schrägbankdrücken (LH)"))
        sm.add_widget(Brustpresse(name="Brustpresse"))
        sm.add_widget(Schulterpresse(name="Schulterpresse"))
        sm.add_widget(Butterfly(name="Butterfly"))
        sm.add_widget(Latzug(name="Latzug"))
        sm.add_widget(Fahrradtrainer(name="Fahrradtrainer"))
        sm.add_widget(Beinpresse(name="Beinpresse"))
        sm.add_widget(Beinstrecker(name="Beinstrecker"))
        sm.add_widget(Kreuzheben(name="Kreuzheben"))
        sm.add_widget(KniebeugenKH(name="Kniebeugen (LH)"))
        sm.add_widget(Laufband(name="Laufband"))
        sm.add_widget(mehr(name="mehr"))
        return sm
        return layout_vertical

if __name__ == "__main__":
    GymNotizApp().run()