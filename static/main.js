
const weekdays = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"];
menus = null;

async function fetchMenus()
{
    const res = await fetch("./menus.json", {cache: "no-cache"});
    menus = await res.json();
    const updatedSpan = document.getElementById("updated");
    updatedSpan.innerHTML = menus.updated;
    updateMenu(getCurrentDayIndex());
}

function getCurrentDayIndex()
{
    let dayIndex = new Date().getDay();
    // No weekend for you
    if (dayIndex == 0 || dayIndex == 6)
    {
        dayIndex = 5;
    } 
    return dayIndex;
}

function updateMenu(dayIndex)
{
    const day = weekdays[dayIndex];
    const buttons = document.getElementsByClassName("button-day");
    const activeClass = "button-active";
    for (let button of buttons)
    {
        if (button.classList.contains(activeClass))
        {
            button.classList.remove(activeClass);
        }
    }
    buttons[dayIndex - 1].classList.add(activeClass);
    const container = document.getElementById("container")
    container.replaceChildren(...getMenuDivs(day))
}

function getMenuDivs(day)
{
    const dayMenus = [];
    for (const menu of menus.menus)
    {
        const div = document.createElement("div");
        div.className = "item";
        let h2 = document.createElement("h2");
        h2.innerText = menu.name;
        div.appendChild(h2);
        const ul = document.createElement("ul");
        div.appendChild(ul)
        for (const course of menu.menu[day])
        {
            let li = document.createElement("li");
            li.innerText = course;
            ul.appendChild(li);
        }
        dayMenus.push(div);
    }
    return dayMenus;
}