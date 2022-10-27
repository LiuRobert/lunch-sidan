menus = null;

function getCurrentDay()
{
    const weekday = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"];
    let dayIndex = new Date().getDay();
    // No weekend for you
    if (dayIndex == 0 || dayIndex == 6)
    {
        dayIndex = 1;
    } 
    return weekday[dayIndex];
}

async function fetchMenus()
{
    const res = await fetch("./menus.json", {cache: "no-cache"});
    menus = await res.json();
    const updatedSpan = document.getElementById("updated");
    updatedSpan.innerHTML = menus.updated;
    updateDay(getCurrentDay());
}

async function updateDay(day)
{
    const container = document.getElementById("container")
    for (const menu of menus.menus)
    {
        if (menu.failed)
        {
            continue;
        }
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
        container.appendChild(div);
    }
}