const scrollingElement = (document.scrollingElement || document.body);
scrollingElement.scrollTop = scrollingElement.scrollHeight;
const fnScroll = () => {
    scrollingElement.scrollTop = scrollingElement.scrollHeight;
    setTimeout(fnClick, 2000);
};
const fnClick = () => {
    const btn = document.querySelector("button[aria-label='Show more']");
    if (btn) {
        btn.click();
        setTimeout(fnScroll, 2000);
    } else {
        setTimeout(fnExtr, 2000);
    }
};
const fnExtr = () => {
    const rows = ["PackageName"];
    const ahrefs = document.querySelectorAll("a[jslog]");
    for (const ahref of ahrefs) {
        const pkg = ahref.href.replace('https://play.google.com/store/apps/details?id=', '')
            .replace('/store/apps/details?id=', '');
        rows.push(pkg);
    }
    console.info('Apps found: ', rows.length);
    setTimeout(() => {
        console.log(rows.join("\n"));
        const link = document.createElement("a");
        link.setAttribute("href", "data:text/csv;charset=utf-8," + encodeURIComponent(rows.join("\n")));
        link.setAttribute("download", "app-ids.csv");
        document.body.appendChild(link);
        link.click();
    }, 1000);
};
setTimeout(fnScroll, 250);
// -------------------------------------
// sort app-ids.csv app-ids-2.csv | uniq 