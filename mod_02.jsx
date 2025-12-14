/**
 * @title Module 2: CSV to PSD
 * @version 1.0
 * @author tlcpineda.projects@gmail.com
 * @description Transfer the contents of the CSV file to corresponding PSD files, ready for manual adjustments.
 */

#target: photoshop
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


/**
 * Transform the string content of a CSV file to an array.
 * @param {string} csv_str The contents of the CSV file
 * @returns {Array} csv_arr An array representing the contents of the CSV file with each line as an element of the array.
 */
function parse_csv(csv_str) {
    var csv_arr = [];
    var lines = csv_str.split(/\r\n|\n/);

    // Truncate header row.
    for (var i=1; i<lines.length; i++) {
        var lines_split = lines[i].split(',');

        if (lines_split.length<6) continue; // Stop processing the line, possibly malformed.

        var text = lines_split.slice(5).join(',');
        var replacement_arr = [
            ['""', '"'],
            ['<>', '\r'],
            ['\\.\\.', '...']
        ]

        var line = lines_split.slice(0, 5);
        var is_valid = true;

        // Convert items to float, except the first (remains as string).
        for (var k=1; k<line.length; k++) {
            var val = parseFloat(line[k]);

            // Check if conversion
            if (isNaN(val)) {
                is_valid = false;
                break;
            } else {
                line[k] = val;
            }
        }

        if (!is_valid) continue; // Stop processing the line, possibly malformed.

        // Strip enclosing quotation marks.
        var text_terminal = text.length - 1;

        if (text.charAt(0)==='"' && text.charAt(text_terminal)==='"') {
            text = text.substring(1, text_terminal);
        }

        // Clean up text.
        for (var j=0; j<replacement_arr.length; j++ ) {
            text = text.replace(new RegExp(replacement_arr[j][0], 'g'), replacement_arr[j][1]);
        }

        csv_arr.push(line.concat([text]));
    }

    return csv_arr
}

// Run the main function.
main();