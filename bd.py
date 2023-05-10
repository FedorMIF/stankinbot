import asyncpg
import asyncio
from config import DATABASE_CONFIG
import log

async def create_connection():
    return await asyncpg.connect(**DATABASE_CONFIG)

async def create_tables():
    conn = await create_connection()
    try:
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            user_id INT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            "group" TEXT,
            role_group TEXT,
            phone TEXT,
            email TEXT
        );
    ''')
        await conn.close()
        return True
    except Exception as e:
        await conn.close()
        await log.add(str(e))
        return False

async def add_new_user(name, user_id, role):
    conn = await create_connection()
    await conn.execute('''
        INSERT INTO users (user_id, name, role) VALUES ($1, $2, $3);
    ''', user_id, name,role)
    await conn.close()

async def edit_user_name(name, user_id):
    conn = await create_connection()
    await conn.execute('''
        UPDATE users SET name = $1 WHERE user_id = $2;
    ''', name, user_id)
    await conn.close()

async def edit_user_role(user_id, name, role, group, role_group, phone, email):
    conn = await create_connection()
    await conn.execute('''
        UPDATE users SET name = $1, role = $2, "group" = $3, role_group = $4, phone = $5, email = $6 WHERE user_id = $7;
    ''', name, role, group, role_group, phone, email, user_id)

async def give_user_name(user_id):
    conn = await create_connection()
    result = await conn.fetchrow('''
        SELECT name, role FROM users WHERE user_id = $1;
    ''', user_id)
    await conn.close()
    return result["name"], result['role']

async def get_list_users():
    conn = await create_connection()
    result = await conn.fetch('''
        SELECT user_id, name, role FROM users;
    ''')
    await conn.close()
    return result

async def get_admins():
    conn = await create_connection()
    result = await conn.fetch('''
        SELECT user_id FROM users WHERE role = 'Администратор';
    ''')
    return [row['user_id'] for row in result]