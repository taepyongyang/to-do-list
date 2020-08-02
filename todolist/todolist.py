from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def get_id(self):
        return self.id

    def get_deadline(self):
        return self.deadline

    def get_task(self):
        return self.task

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def db_add_task(dbsession, new_task, new_deadline):
    new_row = Task(task=new_task,
                   deadline=new_deadline)
    dbsession.add(new_row)
    dbsession.commit()
    print('The task has been added!')


def db_del_task(dbsession, id_to_delete):
    dbsession.query(Task).filter(Task.id == id_to_delete).delete()
    dbsession.commit()
    print('The task has been added!')


def print_menu():
    todo = ["Today's tasks",
            "Week's tasks",
            "All tasks",
            "Missed tasks",
            "Add task",
            "Delete task"]

    for i in range(len(todo)):
        print('{}) {}'.format(i + 1, todo[i]))
    print('0) Exit')


def menu_todays_tasks(dbsession):
    today = datetime.today().date()
    rows = dbsession.query(Task).filter(Task.deadline == today).all()

    print(f'Today {today.strftime("%e %b")}:')

    if not rows:
        print('Nothing to do!')
    else:
        for i in rows:
            print('{}'.format(i))
    print()


def menu_add_task(dbsession):
    task = input("Enter task\n")
    deadline = input("Enter deadline\n")
    deadline = datetime.strptime(deadline, "%Y-%m-%d").date()
    db_add_task(dbsession, task, deadline)


def menu_missed_task(dbsession):
    today = datetime.today().date()
    rows = dbsession.query(Task).filter(Task.deadline < today).all()

    print('Missed tasks:')

    index = 1
    if rows:
        for row in rows:
            day_of_month = int(row.get_deadline().strftime('%e'))
            print('{}. {}. {} {}'.format(index, row, day_of_month, row.get_deadline().strftime("%b")))
            index += 1
    else:
        print('Nothing is missed!')
    print()


def menu_weeks_tasks(dbsession):
    today = datetime.today()
    a_week_from_today = today + timedelta(days=6)
    day_index = today
    while day_index <= a_week_from_today:
        print('{}:'.format(day_index.strftime('%A%e %b')))
        rows = dbsession.query(Task).filter(Task.deadline == day_index.date()).all()
        if rows:
            index = 1
            for row in rows:
                print('{}. {}'.format(index, row))
                index += 1
        else:
            print('Nothing to do!')
        day_index += timedelta(days=1)
        print()


def menu_all_tasks(dbsession, header_text='All tasks:'):
    rows = dbsession.query(Task).order_by(Task.deadline).all()

    index = 1

    print(header_text)
    if rows:
        for row in rows:
            day_of_month = int(row.get_deadline().strftime('%e'))
            print('{}. {}. {} {}'.format(index, row, day_of_month, row.get_deadline().strftime("%b")))
            index += 1
    print()


def menu_delete_task(dbsession):
    rows = dbsession.query(Task).order_by(Task.deadline).all()

    index = 1

    db_id_lookup = {}

    print('Choose the number of the task you want to delete:')

    if rows:
        for row in rows:
            day_of_month = int(row.get_deadline().strftime('%e'))
            print('{}. {}. {} {}'.format(index, row, day_of_month, row.get_deadline().strftime("%b")))
            db_id_lookup[index] = row.get_id()
            index += 1

        id_to_delete = db_id_lookup[int(input())]

        db_del_task(dbsession, id_to_delete)
    print()


def show_menu():
    choice = None
    while choice != 0:
        print_menu()
        choice = int(input())
        if choice == 0:
            print('\nBye!')
        elif choice == 1:
            menu_todays_tasks(session)
        elif choice == 2:
            menu_weeks_tasks(session)
        elif choice == 3:
            menu_all_tasks(session)
        elif choice == 4:
            menu_missed_task(session)
        elif choice == 5:
            menu_add_task(session)
        elif choice == 6:
            menu_delete_task(session)


show_menu()
