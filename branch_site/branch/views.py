import json
from bardapi import Bard

import os
# views.py
from django.shortcuts import render
from .models import Peoples, Relationships
from .forms import SearchForm
token = 'bwiC9Ly3rPxfrUiU-3qoNV6ILig-jvMDlRNBOYnE_K0_jL95l7Ucd4D1jx3vWUkaW6B4Zw.'
os.environ["_BARD_API_KEY"] = token





def search(request):


    full_name = None
    born_date = None
    death_date = None
    source_link = None
    parents = None
    children = None

    if request.method == 'POST':
        # Process the form when it's submitted
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']

            # Search for the person by name
            try:
                person = Peoples.objects.get(full_name=name)
                # Retrieve fields directly from the person object
                search_person_id = person.id


                parents = Relationships.objects.filter(child=person).values_list('parent__full_name', flat=True)
                children = Relationships.objects.filter(parent=person).values_list('child__full_name', flat=True)
            except Peoples.DoesNotExist:

                # JSON
                message = "In JSON (full_name, born_date, death_date, father, mother, children, source_link)  " \
                          "format explain. If some information is unknown leave empty(null)." \
                          "Father, mother, children just a full name. For the person {}?".format(name)
                bard_search_engine(message)

            else:
                # check validation data

                source_link = person.source_link
                if source_link is not None:
                    full_name = person.full_name
                    born_date = person.born_date
                    death_date = person.death_date
                if source_link is None:
                    update_person_info(search_person_id, name)


    else:
        form = SearchForm()

    return render(request, 'search.html', {
        'form': form,
        'full_name': full_name,
        'born_date': born_date,
        'death_date': death_date,
        'source_link': source_link,
        'parents': parents,
        'children': children
    })

def bard_search_engine(message):
    content = Bard().get_answer(str(message))['content']
    print(content)
    start_pos = content.find("{")
    end_pos = content.find("}")
    content_json = content[start_pos:end_pos + 1].strip()
    data_dict = json.loads(content_json, strict=False)
    json_to_sql(data_dict)


def json_to_sql(data_dict):
    try:
        full_name = data_dict["full_name"]
        full_name = full_name.replace(" Jr.", "").replace(" Sr.", "")
        split_full_name = full_name.split()
        if len(split_full_name) > 2:
            first_name = split_full_name[0]
            last_name = split_full_name[-1]
            full_name = f"{first_name} {last_name}"
        else:
            full_name = full_name

        born_date = data_dict["born_date"]

        death_date = data_dict["death_date"]

        father = data_dict["father"]
        if father is None:
            pass
        else:
            father = father.replace(" Jr.", "").replace(" Sr.", "")
            split_father = father.split()
            if len(split_father) > 2:
                first_name = split_father[0]
                last_name = split_father[-1]
                father = f"{first_name} {last_name}"
            else:
                father = father

        mother = data_dict["mother"]
        if mother is None:
            pass
        else:
            mother = mother.replace(" Jr.", "").replace(" Sr.", "")
            split_mother = mother.split()
            if len(mother) > 2:
                first_name = split_mother[0]
                last_name = split_mother[-1]
                mother = f"{first_name} {last_name}"
            else:
                mother = mother

        children = data_dict["children"]
        childrens = []
        if children is None:
            pass
        else:
            for child in children:
                child = child.replace(" Jr.", "").replace(" Sr.", "")
                split_child = child.split()
                if len(child) > 2:
                    first_name = split_child[0]
                    last_name = split_child[-1]
                    child = f"{first_name} {last_name}"
                    childrens.append(child)
                else:
                    child = child
                    childrens.append(child)

        source_link = data_dict["source_link"]

        # ADD main person

        try:
            # check person id in DB
            person = Peoples.objects.get(full_name=full_name)

            # Retrieve fields directly from the person object
            person.full_name = full_name
            person.born_date = born_date
            person.death_date = death_date
            person.source_link = source_link
            person.save()
        except Peoples.DoesNotExist:
            # Person not found, so add a new person
            new_person = Peoples(
                full_name=full_name,
                born_date=born_date,  # Assuming you have this value
                death_date=death_date,  # Assuming you have this value
                source_link=source_link,  # Assuming you have this value
            )
            new_person.save()
        # ID main person

        id_main_person = Peoples.objects.get(full_name=full_name)
        id_main_person = id_main_person.id
        # ADD father main person

        if father is None:
            pass
        else:
            try:
                # check person id in DB
                search_person_id = Peoples.objects.get(full_name=father)
                search_person_id = search_person_id.id
                new_relationships = Relationships(
                    parent_id=search_person_id,
                    child_id=id_main_person
                )
                new_relationships.save()
            except Peoples.DoesNotExist:
                add_father = Peoples(full_name=father)
                add_father.save()  # Save the new family member to the database
                # Retrieve the ID of the newly added father
                id_father = add_father.id
                new_relationships = Relationships(
                    parent_id=id_father,
                    child_id=id_main_person
                )
                new_relationships.save()

        if mother is None:
            pass
        else:
            try:
                # check person id in DB
                search_person_id = Peoples.objects.get(full_name=mother)
                search_person_id = search_person_id.id
                new_relationships = Relationships(

                    parent_id=search_person_id,
                    child_id=id_main_person
                )
                new_relationships.save()
            except Peoples.DoesNotExist:
                add_mother = Peoples(full_name=mother)
                add_mother.save()  # Save the new family member to the database
                # Retrieve the ID of the newly added father
                id_mother = add_mother.id
                new_relationships = Relationships(

                    parent_id=id_mother,
                    child_id=id_main_person
                )
                new_relationships.save()

        # ADD children main person
        # Loop through each child and add them to the main person's family
        if children is None:
            pass
        else:
            for child in childrens:
                try:
                    search_person_id = Peoples.objects.get(full_name=child)
                    search_person_id = search_person_id.id
                    new_child_relationships = Relationships(

                        parents_id=id_main_person,
                        child_id=search_person_id
                    )
                    new_child_relationships.save()
                except Peoples.DoesNotExist:
                    new_person = Peoples(full_name=child)
                    new_person.save()
                    search_person_id = Peoples(full_name=child)
                    search_person_id = search_person_id.id
                    # Create the relationship between the main person and the child
                    new_child_relationships = Relationships(

                        parents_id=id_main_person,
                        child_id=search_person_id
                    )
                    new_child_relationships.save()
    finally:
        return SearchForm(full_name)


def update_person_info(search_person_id, name):
    try:
        parent = Relationships.objects.filter(child__id=search_person_id).values_list(
            'parent__full_name',
            flat=True)
        # JSON
        message = (
            "In JSON (full_name, born_date, death_date, father, mother, children, source_link) format explain. "
            "If some information is unknown, leave empty (null)."
            "Father, mother, children just a full name."
            "For the person: {}, parent(s): {}"
                .format(name, parent, "parent" if " and " not in parent else "parents"))
        bard_search_engine(message)
    except IndexError:
        childrens = Relationships.objects.filter(parent__id=search_person_id).values_list(
            'child__full_name', flat=True)
        child_names = [children[2] for children in childrens]
        # JSON
        message = (
            "In JSON (full_name, born_date, death_date, father, mother, children, source_link) format explain. "
            "If some information is unknown, leave empty (null). "
            "Father, mother, children just a full name."
            "For the person: {} is a parent for: {}"
                .format(name, child_names, "parent" if " and " not in child_names else "parents")
        )
        bard_search_engine(message)
