// target photoshop

function main() {
    var doc = app.activeDocument;

    // 2. Identify CSV location
    // Path logic: PSD is in "2 TYPESETTING", CSV is in the parent folder
    var psdFolder = doc.path;
    var parentFolder = psdFolder.parent;
    var csvFile = new File(parentFolder + "/translations.csv");

    if (!csvFile.exists) {
        // Log error to a file if needed, but don't use 'alert'
        return;
    }

    // 3. Read CSV Content
    csvFile.open('r');
    csvFile.encoding = "UTF-8";
    var content = csvFile.read();
    csvFile.close();

    var lines = content.split(/\r\n|\n/);

    // 4. Extract Page ID from PSD Filename (Last 2 digits before extension)
    // Matches your naming: MyMangaTitle_..._05.psd
    var docName = doc.name.split('.')[0];
    var pageID = docName.substring(docName.length - 2);

    // 5. Process CSV Lines
    for (var i = 1; i < lines.length; i++) {
        if (lines[i] == "") continue;

        var columns = parseCSVLine(lines[i]);
        var csvPageNum = columns[0].substring(0, 2); // Get "05" from "05X"

        // Only process if CSV row matches current PSD page
        if (csvPageNum === pageID) {
            var x0 = parseFloat(columns[1]);
            var y0 = parseFloat(columns[2]);
            var w_norm = parseFloat(columns[4]);
            var h_norm = parseFloat(columns[5]);
            var text = columns[6].replace(/ <>/g, "\r");

            createParagraphText(doc, text, x0, y0, w_norm, h_norm);
        }
    }
}

function createParagraphText(doc, content, x0, y0, w_norm, h_norm) {
    var newLayer = doc.artLayers.add();
    newLayer.kind = LayerKind.TEXT;
    var textItem = newLayer.textItem;

    // Convert to 'Paragraph Text' to use the bounding box
    textItem.kind = TextType.PARAGRAPHTEXT;

    // Calculate dimensions based on PSD size
    var docW = doc.width.as("px");
    var docH = doc.height.as("px");

    textItem.width = w_norm * docW;
    textItem.height = h_norm * docH;

    // Position (Top-Left of the box)
    textItem.position = [x0 * docW, y0 * docH];

    textItem.contents = content;

    // Logic for RTL/Manga: Center-aligned is often preferred for balloons
    textItem.justification = Justification.CENTER;
}

// Helper to handle CSV quotes and commas
function parseCSVLine(line) {
    var pattern = /("([^"]|"")*"|[^,]*)(,|$)/g;
    var matches = line.match(pattern);
    var result = [];
    for (var i = 0; i < matches.length; i++) {
        var val = matches[i].replace(/,$/, "");
        result.push(val.replace(/^"|"$/g, "").replace(/""/g, '"'));
    }
    return result;
}

main();