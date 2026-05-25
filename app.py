import datetime
import gradio as gr
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sqlalchemy import text, create_engine

# Tự động cấu hình CSDL SQLite chạy trực tiếp để test giao diện
DATABASE_URI = "sqlite:///management_db.db"
engine = create_engine(DATABASE_URI)


def initialize_database():
    with engine.connect() as conn:
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100),
                category VARCHAR(50),
                price FLOAT
            );
        """)
        )
        conn.execute(
            text("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INT,
                quantity INT,
                order_date DATE,
                total_price FLOAT
            );
        """)
        )
        conn.commit()

        check_products = pd.read_sql(
            "SELECT COUNT(*) FROM products", conn
        ).iloc[0, 0]
        if check_products == 0:
            conn.execute(
                text("""
                INSERT INTO products (name, category, price) VALUES
                ('Laptop Dell XPS', 'Điện tử', 1500),
                ('iPhone 15 Pro', 'Điện tử', 1000),
                ('Bàn phím cơ Razer', 'Phụ kiện', 120),
                ('Chuột Logitech G502', 'Phụ kiện', 70);
            """)
            )
            conn.commit()


initialize_database()


def get_products_dataframe():
    return pd.read_sql(
        "SELECT id, name, category, price FROM products ORDER BY id ASC", engine
    )


def get_orders_dataframe():
    query = """
        SELECT o.id, p.name AS product_name, o.quantity, o.order_date, o.total_price 
        FROM orders o
        JOIN products p ON o.product_id = p.id
        ORDER BY o.id DESC
    """
    return pd.read_sql(query, engine)


X_train = np.array(
    [
        [1, 70],
        [2, 70],
        [5, 120],
        [1, 1000],
        [2, 1000],
        [1, 1500],
        [2, 1500],
        [10, 120],
    ]
)
y_train = np.array([70, 140, 600, 1000, 2000, 1500, 3000, 1200])
ml_model = LinearRegression().fit(X_train, y_train)


def predict_order_value(quantity, unit_price):
    prediction = ml_model.predict(np.array([[float(quantity), float(unit_price)]]))[0]
    return f"Giá trị đơn hàng dự báo là: ${round(prediction, 2)}"


with gr.Blocks(title="Hệ thống Quản lý Đơn hàng") as demo:
    gr.Markdown("# 📊 HỆ THỐNG QUẢN LÝ VÀ DỰ BÁO ĐƠN HÀNG")
    with gr.Tab("📋 Xem dữ liệu Hệ thống"):
        btn_refresh = gr.Button("🔄 Tải / Làm mới Dữ liệu", variant="primary")
        table_products = gr.Dataframe()
        table_orders = gr.Dataframe()
        btn_refresh.click(
            fn=get_products_dataframe, outputs=table_products
        ).then(fn=get_orders_dataframe, outputs=table_orders)
    with gr.Tab("🤖 Dự Báo Bằng AI (Machine Learning)"):
        with gr.Row():
            ml_quantity = gr.Slider(
                minimum=1, maximum=100, step=1, label="Số lượng", value=5
            )
            ml_price = gr.Number(label="Đơn giá ($)", value=120)
        btn_predict = gr.Button("🧠 Chạy mô hình dự báo", variant="primary")
        output_prediction = gr.Textbox(label="Kết quả dự báo")
        btn_predict.click(
            fn=predict_order_value,
            inputs=[ml_quantity, ml_price],
            outputs=output_prediction,
        )

if __name__ == "__main__":
    demo.launch()
