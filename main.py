import flet as ft
import pyautogui
import keyboard
import threading
import asyncio
import time
from typing import Optional

class AutoClicker:
    def __init__(self):
        self.is_running = False
        self.click_thread: Optional[threading.Thread] = None
        self.interval = 1.0  # デフォルトのクリック間隔（秒）

    def toggle_clicking(self):
        if not self.is_running:
            self.is_running = True
            self.click_thread = threading.Thread(target=self._click_loop)
            self.click_thread.daemon = True
            self.click_thread.start()
        else:
            self.is_running = False
            if self.click_thread:
                self.click_thread.join(timeout=1.0)

    def _click_loop(self):
        while self.is_running:
            pyautogui.click()
            time.sleep(self.interval)

def main(page: ft.Page):
    page.title = "Auto Clicker"
    # page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.auto_scroll = True
    page.window.width = 300  # 幅
    page.window.height = 500  # 高さ
    
    # オートクリッカーのインスタンスを作成
    auto_clicker = AutoClicker()
    
    # ステータステキスト
    status_text = ft.Text("Status: Stopped", size=20)
    
    # インターバル入力
    interval_input = ft.TextField(
        label="Click Interval (seconds)",
        value="1.0",
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    def update_interval(e):
        try:
            new_interval = float(interval_input.value)
            if new_interval > 0:
                auto_clicker.interval = new_interval
        except ValueError:
            pass

    interval_input.on_change = update_interval
    
    # ホットキー設定のテキストフィールド
    hotkey_input = ft.TextField(
        label="Hotkey",
        value="ctrl+shift+a",
        width=200
    )
    
    def on_hotkey_press():
        auto_clicker.toggle_clicking()
        status_text.value = "Status: Running" if auto_clicker.is_running else "Status: Stopped"
        page.update()
    
    def update_hotkey(e):
        keyboard.remove_all_hotkeys()
        try:
            keyboard.add_hotkey(hotkey_input.value, on_hotkey_press)
        except ValueError as e:
            hotkey_input.value = "ctrl+shift+a"
            hotkey_error_test_field.value = "Hot key error return default"
            page.update()
            keyboard.add_hotkey("ctrl+shift+a", on_hotkey_press)

            # 10 秒後にエラーを削除
            asyncio.run(delay_task(10))

    hotkey_input.on_submit = update_hotkey
    
    # hotkey error 表示用
    async def delayed_delete_error_text(seconds):
        await asyncio.sleep(seconds)
        hotkey_error_test_field.value=""
    
    async def delay_task(seconds):
        delay_task = asyncio.create_task(delayed_delete_error_text(seconds))
        await delay_task
        page.update()

    hotkey_error_test_field = ft.Text(
        value=""
    )
    
    # 初期ホットキーの設定
    keyboard.add_hotkey(hotkey_input.value, on_hotkey_press)
    
    # レイアウトの設定
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Auto Clicker", size=30, weight=ft.FontWeight.BOLD),
                    status_text,
                    ft.Text("Settings:", size=20),
                    interval_input,
                    hotkey_input,
                    hotkey_error_test_field,
                    ft.Text(
                        "Press the hotkey to start/stop auto-clicking",
                        size=14,
                        color=ft.colors.GREY_700
                    ),
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=30
        )
    )

if __name__ == "__main__":
    ft.app(target=main)