from todoapp.models import User, Item


def gen_user(
        username="foobar",
        first_name="Foobariasz",
        last_name="Barusowicz",
        email="foo@bar.test.com",
        password="P@ssw0rd!"
    ):
    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
    )
    user.set_password(password)
    user.save()

    return user

def gen_item(
        title="create new endpoint",
        text="add new endpoint to the app",
        status="to do",
        category="task",
        due_date="2022-05-06T00:00:00Z",
        owner_id=1,
        creator_id=1
    ):
    item = Item(
        title=title,
        text=text,
        status=status,
        due_date=due_date,
        owner_id=owner_id,
        creator_id=creator_id
    )
    item.save()

    return item