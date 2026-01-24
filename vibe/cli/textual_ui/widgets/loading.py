from __future__ import annotations

from datetime import datetime
import random
from time import time
from typing import ClassVar

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static

from vibe.cli.textual_ui.widgets.no_markup_static import NoMarkupStatic
from vibe.cli.textual_ui.widgets.spinner import SpinnerMixin, SpinnerType


class LoadingWidget(SpinnerMixin, Static):
    TARGET_COLORS = ("#FFD800", "#FFAF00", "#FF8205", "#FA500F", "#E10500")
    SPINNER_TYPE = SpinnerType.CIRCLE

    EASTER_EGGS: ClassVar[list[str]] = [
        # Citations pures
        "Tiens, ça c'est de la soupe aux choux, de la vraie, faite avec mes choux à moi",
        "Gamin, on attaque !",
        "J'm'embête pas avec toi la Denrée, quand je pète tu rappliques d'on ne sait pas où",
        "Maintenant on va attendre un peu, que ça prenne bien le bouillon",
        "La soupe au choux mon Blaise, ça parfume jusqu'au trognon",
        "Et voilà mon gars, t'es calé pour la route !",
        "Oh c'est t'y bon mon Glaude",
        "Mon eau, elle a une température de haute précision pour l'perniflard, au degré près",
        "Si c'est glacé, ça t'tranche l'ventre, mais là ça t'descends dans les boyaux comme la rosée du matin sur les feuilles",
        "Haut les mains, Judas !",
        "Maintenant j'vais t'faire passer la cafetière au travers du mur !",
        "Bon, bah c'est pas tout l'père, mais tu me retarde",
        "L'heure c'est l'heure, et c'est l'heure du perniflard, j'va m'en enfiler une larmichette",
        "C'est pas possible... J'suis pourtant pas plein !",
        "J'l'ai vu c'te soucoupe, j'l'ai vu... avec mes yeux j'l'ai vu",
        "Eh ben, t'as dû en vider des tonneaux de pinard pendant que j'étais pas là",
        "Eh ben mes p'tits frères, ça commence bien",
        "T'as couché avec le Bombé ?!",
        # Inventions ou détournement de répliques
        "Faut aérer... ça sent le renfermé dans ce serveur",
        "Je vous sers un petit canon en attendant la réponse ?",
        "C'est pas de la soupe en sachet ça, c'est de la vraie !",
        "Y'a quelqu'un ? Y'a du monde dans les tuyaux ?",
        "Doucement... Faut pas me bousculer pendant la digestion",
        "Je regarde là-haut... Des fois qu'ils reviendraient",
        "Ça a quel goût ? Ça a un goût de reviens-y !",
        "Attention au Bombé, il arrive avec son litron",
        "Je suis en train de te préparer une soupe aux choux maison",
        "Déploiement vers la planète Oxo... Glou glou !",
        "Nettoyage de la mémoire : on ne gâche rien, les restes ça va dans la soupe",
        "Ce module est plus vieux que la Francine, mais il tient encore debout",
        "Envoi des données dans le nuage... Enfin, dans la soucoupe",
        "Je tourne en rond comme le facteur qui a bu trop de perniflard",
        "Laisse mijoter le binaire... faut que ça bout doucement",
        "Compilation réussie ! Ca s'arrose au perniflard !",
    ]

    EASTER_EGGS_HALLOWEEN: ClassVar[list[str]] = [
        "Des bonbons ou un litron ?",
        "Chasse aux bugs fantômes... Wouuuh !",
        "La Francine est sortie de sa boîte !",
        "C'est pas un loup-garou, c'est le Bombé qui a soif !",
        "Invocation de démons... heu, de daemons Linux",
        "C'est pas une citrouille, c'est un chou mutant !",
        "Déploiement effrayant vers la planète Oxo",
    ]

    EASTER_EGGS_DECEMBER: ClassVar[list[str]] = [
        "Petit Papa Glaude... apporte-moi un code sans bug",
        "Ça caille ! Remets une bûche dans le serveur !",
        "Joyeux Noël ! J'ai mis des Louis d'or dans le code",
        "Emballage des paquets Python au pied du sapin",
        "La soupe fume sur le feu... compilez en paix",
        "Menu de réveillon : Dinde farcie aux octets",
        "Il neige dans le terminal... mettez vos bonnets",
        "Y'a pas que la dinde qui est fourrée, le cache aussi !",
        "On attend le Père Noël ou la Denrée ? Dans le doute, je sers la soupe",
        "Sortez les guirlandes RGB, on va tuner le terminal !",
        "On boira le canon après le déploiement de minuit",
        "Glou glou 'Festive Edition' : La soupe au champagne !",
        "J'entends les cloches... ah non, c'est l'alerte CPU",
        "Attention au verglas sur le bus de données, ça glisse !",
        "J'ai demandé un GPU au Père Noël, l'autre a fondu à l'inférence",
        "Le sapin clignote comme un serveur en panne, c'est beau",
        "Chants de Noël en 8-bit interprétés par la Denrée",
        "C'est l'heure d'ouvrir les cadeaux... ou les Pull Requests !",
        "Il fait froid dehors, mais le processeur me tient chaud",
    ]

    def __init__(self, status: str | None = None) -> None:
        super().__init__(classes="loading-widget")
        self.init_spinner()
        self.status = status or self._get_default_status()
        self.current_color_index = 0
        self.transition_progress = 0
        self._status_widget: Static | None = None
        self.hint_widget: Static | None = None
        self.start_time: float | None = None
        self._last_elapsed: int = -1

    def _get_easter_egg(self) -> str | None:
        EASTER_EGG_PROBABILITY = 1.0
        if random.random() < EASTER_EGG_PROBABILITY:
            available_eggs = list(self.EASTER_EGGS)

            OCTOBER = 10
            HALLOWEEN_DAY = 31
            DECEMBER = 12
            now = datetime.now()
            if now.month == OCTOBER and now.day == HALLOWEEN_DAY:
                available_eggs.extend(self.EASTER_EGGS_HALLOWEEN)
            if now.month == DECEMBER:
                available_eggs.extend(self.EASTER_EGGS_DECEMBER)

            return random.choice(available_eggs)
        return None

    def _get_default_status(self) -> str:
        return self._get_easter_egg() or "Generating"

    def _apply_easter_egg(self, status: str) -> str:
        return self._get_easter_egg() or status

    def set_status(self, status: str) -> None:
        self.status = self._apply_easter_egg(status)
        self._update_animation()

    def compose(self) -> ComposeResult:
        with Horizontal(classes="loading-container"):
            self._indicator_widget = Static(
                self._spinner.current_frame(), classes="loading-indicator"
            )
            yield self._indicator_widget

            self._status_widget = Static("", classes="loading-status")
            yield self._status_widget

            self.hint_widget = NoMarkupStatic(
                "(0s esc to interrupt)", classes="loading-hint"
            )
            yield self.hint_widget

    def on_mount(self) -> None:
        self.start_time = time()
        self._update_animation()
        self.start_spinner_timer()

    def on_resize(self) -> None:
        self.refresh_spinner()

    def _update_spinner_frame(self) -> None:
        if not self._is_spinning:
            return
        self._update_animation()

    def _get_color_for_position(self, position: int) -> str:
        current_color = self.TARGET_COLORS[self.current_color_index]
        next_color = self.TARGET_COLORS[
            (self.current_color_index + 1) % len(self.TARGET_COLORS)
        ]
        if position < self.transition_progress:
            return next_color
        return current_color

    def _build_status_text(self) -> str:
        parts = []
        for i, char in enumerate(self.status):
            color = self._get_color_for_position(1 + i)
            parts.append(f"[{color}]{char}[/]")
        ellipsis_start = 1 + len(self.status)
        color_ellipsis = self._get_color_for_position(ellipsis_start)
        parts.append(f"[{color_ellipsis}]… [/]")
        return "".join(parts)

    def _update_animation(self) -> None:
        total_elements = 1 + len(self.status) + 1

        if self._indicator_widget:
            spinner_char = self._spinner.next_frame()
            color = self._get_color_for_position(0)
            self._indicator_widget.update(f"[{color}]{spinner_char}[/]")

        if self._status_widget:
            self._status_widget.update(self._build_status_text())

        self.transition_progress += 1
        if self.transition_progress > total_elements:
            self.current_color_index = (self.current_color_index + 1) % len(
                self.TARGET_COLORS
            )
            self.transition_progress = 0

        if self.hint_widget and self.start_time is not None:
            elapsed = int(time() - self.start_time)
            if elapsed != self._last_elapsed:
                self._last_elapsed = elapsed
                self.hint_widget.update(f"({elapsed}s esc to interrupt)")
