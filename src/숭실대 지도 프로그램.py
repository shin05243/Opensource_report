import folium
import tkinter as tk
import webbrowser
import json
from folium.plugins import MiniMap

DATA_FILE = 'locations.json'


def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as file:
        json.dump(custom_locations, file, ensure_ascii=False, indent=4)

def merge_data(initial_data, loaded_data):
    for category, locations in loaded_data.items():
        if category in initial_data:
            initial_data[category].extend(locations)
        else:
            initial_data[category] = locations
    return initial_data

custom_locations = load_data()

def show_category_map(category):
    m = folium.Map(location=(37.496344, 126.957019), zoom_start=17)
    minimap = MiniMap()
    m.add_child(minimap)

    for info, loc in custom_locations.get(category, []):
        popup_html = f'<div style="white-space: nowrap; text-align:left;"><b>{info["name"]}</b><br>{info["description"]}</div>'
        folium.Marker(location=loc, popup=popup_html, icon=folium.Icon(color='blue')).add_to(m)

    m.save('map.html')
    webbrowser.open_new_tab('map.html')

# Global variable to track the current open window
current_window = None

def close_current_window():
    global current_window
    if current_window is not None:
        current_window.destroy()
        current_window = None

def add_or_update_category():
    close_current_window()
    
    def save_category():
        category = category_var.get()
        if category == '새 카테고리':
            category = new_category_entry.get()
            if not category:
                return
        name = name_entry.get()
        description = description_entry.get() or ""  # 부연 설명이 없으면 빈 문자열로 초기화
        try:
            latitude = float(latitude_entry.get())
            longitude = float(longitude_entry.get())
        except ValueError:
            return

        if category and name and description is not None:
            if category not in custom_locations:
                custom_locations[category] = []
            custom_locations[category].append(({'name': name, 'description': description}, (latitude, longitude)))
            save_data()
            update_category_buttons()
            new_category_window.destroy()

    global current_window
    new_category_window = tk.Toplevel(root)
    new_category_window.title("새 카테고리 추가")
    current_window = new_category_window
    
    # 메인 창 위치
    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()
    
    # 새 창을 메인 창의 오른쪽에 배치
    new_category_window.geometry(f"400x300+{root_x + root_width + 10}+{root_y}")

    tk.Label(new_category_window, text="카테고리 선택 또는 새 카테고리 추가").pack()
    category_var = tk.StringVar(new_category_window)
    category_var.set('카테고리 선택')
    category_options = list(custom_locations.keys()) + ['새 카테고리']
    category_menu = tk.OptionMenu(new_category_window, category_var, *category_options)
    category_menu.pack()

    new_category_entry = tk.Entry(new_category_window)
    new_category_entry.pack()

    tk.Label(new_category_window, text="이름").pack()
    name_entry = tk.Entry(new_category_window)
    name_entry.pack()

    tk.Label(new_category_window, text="부연 설명").pack()
    description_entry = tk.Entry(new_category_window)
    description_entry.pack()

    tk.Label(new_category_window, text="위도").pack()
    latitude_entry = tk.Entry(new_category_window)
    latitude_entry.pack()

    tk.Label(new_category_window, text="경도").pack()
    longitude_entry = tk.Entry(new_category_window)
    longitude_entry.pack()

    save_button = tk.Button(new_category_window, text="저장", command=save_category)
    save_button.pack()

def delete_category():
    close_current_window()
    
    def delete_selected_category():
        category = category_var.get()
        if category in custom_locations:
            del custom_locations[category]
            save_data()
            update_category_buttons()
            delete_category_window.destroy()

    global current_window
    delete_category_window = tk.Toplevel(root)
    delete_category_window.title("카테고리 삭제")
    current_window = delete_category_window

    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()

    delete_category_window.geometry(f"400x200+{root_x + root_width + 10}+{root_y}")

    tk.Label(delete_category_window, text="삭제할 카테고리 선택").pack()
    category_var = tk.StringVar(delete_category_window)
    category_var.set('카테고리 선택')
    category_options = list(custom_locations.keys())
    category_menu = tk.OptionMenu(delete_category_window, category_var, *category_options)
    category_menu.pack()

    delete_button = tk.Button(delete_category_window, text="삭제", command=delete_selected_category)
    delete_button.pack()

def delete_location():
    close_current_window()
    
    def update_location_menu(*args):
        selected_category = category_var.get()
        location_menu['menu'].delete(0, 'end')
        if selected_category in custom_locations:
            for loc in custom_locations[selected_category]:
                location_menu['menu'].add_command(label=loc[0]['name'], command=tk._setit(location_var, loc[0]['name']))

    def delete_selected_location():
        category = category_var.get()
        location_name = location_var.get()
        if category in custom_locations:
            for loc in custom_locations[category]:
                if loc[0]['name'] == location_name:
                    custom_locations[category].remove(loc)
                    if not custom_locations[category]:
                        del custom_locations[category]
                    save_data()
                    update_category_buttons()
                    delete_location_window.destroy()
                    break

    global current_window
    delete_location_window = tk.Toplevel(root)
    delete_location_window.title("장소 삭제")
    current_window = delete_location_window

    root_x = root.winfo_x()
    root_y = root.winfo_y()
    root_width = root.winfo_width()

    delete_location_window.geometry(f"400x200+{root_x + root_width + 10}+{root_y}")

    tk.Label(delete_location_window, text="카테고리 선택").pack()
    category_var = tk.StringVar(delete_location_window)
    category_var.set('카테고리 선택')
    category_options = list(custom_locations.keys())
    category_menu = tk.OptionMenu(delete_location_window, category_var, *category_options)
    category_menu.pack()

    tk.Label(delete_location_window, text="장소 선택").pack()
    location_var = tk.StringVar(delete_location_window)
    location_menu = tk.OptionMenu(delete_location_window, location_var, [])
    location_menu.pack()

    category_var.trace('w', update_location_menu)

    delete_button = tk.Button(delete_location_window, text="삭제", command=delete_selected_location)
    delete_button.pack()

def update_category_buttons():
    for widget in category_buttons_frame.winfo_children():
        widget.destroy()
    for category in custom_locations.keys():
        btn = tk.Button(category_buttons_frame, text=category, command=lambda cat=category: show_category_map(cat))
        btn.pack()

root = tk.Tk()
root.title("카테고리 선택")
root.geometry("400x300+50+50")

title_label = tk.Label(root, text="===찾으시는 장소를 선택해주세요===", font=("Helvetica", 16, "bold"))
title_label.pack()

category_buttons_frame = tk.Frame(root)
category_buttons_frame.pack()

update_category_buttons()

add_category_button = tk.Button(root, text="새 카테고리 추가", command=add_or_update_category)
add_category_button.pack()

delete_category_button = tk.Button(root, text="카테고리 삭제", command=delete_category)
delete_category_button.pack()

delete_location_button = tk.Button(root, text="장소 삭제", command=delete_location)
delete_location_button.pack()

root.attributes('-topmost', True)
root.mainloop()
