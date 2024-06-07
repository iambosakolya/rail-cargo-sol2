import sqlite3
from datetime import datetime
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from ui.style import label_style, btn_style, entry_style


def archive_contract(cursor, conn, contract_id):
    try:
        cursor.execute("BEGIN TRANSACTION")

        cursor.execute("SELECT * FROM Contract "
                       "WHERE contract_id = ?", (contract_id,))
        contract = cursor.fetchone()
        if contract is None:
            CTkMessagebox(message="Contract not found!",
                          icon="cancel",
                          option_1="OK")
            return
        cursor.execute("SELECT * FROM Archive "
                       "WHERE contract_id = ?", (contract_id,))
        if cursor.fetchone() is not None:
            CTkMessagebox(message="Contract already archived!",
                          icon="cancel",
                          option_1="OK")
            return

        (conclusion_date, client_id, dispatcher_id,
         cargo_id, payment_id, itinerary_id) = contract[1:]

        archive_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("INSERT INTO Archive (contract_id, conclusion_date, archive_date) "
                       "VALUES (?, ?, ?)",
                       (contract_id, conclusion_date, archive_date))

        # cursor.execute("DELETE FROM Client "
        #                "WHERE client_id = ?", (client_id,))
        #
        # cursor.execute("DELETE FROM Dispatcher "
        #                "WHERE dispatcher_id = ?", (dispatcher_id,))

        cursor.execute("DELETE FROM Cargo "
                       "WHERE cargo_id = ?", (cargo_id,))

        cursor.execute("DELETE FROM "
                       "Payment WHERE payment_id = ?", (payment_id,))

        cursor.execute("DELETE FROM Itinerary "
                       "WHERE itinerary_id = ?", (itinerary_id,))

        cursor.execute("DELETE FROM Contract "
                       "WHERE contract_id = ?", (contract_id,))

        conn.commit()
        CTkMessagebox(message="Contract archived successfully!", icon="check", option_1="Thanks")
    except sqlite3.Error as e:
        conn.rollback()
        CTkMessagebox(message=f"Error: {str(e)}",
                      icon="cancel",
                      option_1="OK")


def show_archive_dialog(cursor, conn):
    def on_confirm():
        contract_id = entry.get()
        if contract_id.isdigit():
            archive_contract(cursor, conn, int(contract_id))
            dialog.destroy()
        else:
            CTkMessagebox(message="Please enter a valid integer ID.",
                          icon="cancel",
                          option_1="OK")

    dialog = CTk()
    dialog.title("Archive contract")

    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()

    dialog_width = 350
    dialog_height = 150

    x_position = (screen_width - dialog_width) // 2
    y_position = (screen_height - dialog_height) // 2

    dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    dialog.resizable(0, 0)

    screen_frame = CTkFrame(master=dialog, width=350,
                            height=200, fg_color="#897E9B")
    screen_frame.pack_propagate(0)
    screen_frame.pack(expand=True, fill="both")

    label = CTkLabel(screen_frame, text="Enter contract ID for archiving:",
                     **label_style)
    label.pack(pady=10)

    entry = CTkEntry(screen_frame)
    entry.pack(pady=10)

    confirm_btn = CTkButton(screen_frame, text="Confirm",
                            **btn_style, command=on_confirm)
    confirm_btn.pack(pady=10)

    dialog.mainloop()
