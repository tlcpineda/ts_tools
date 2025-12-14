/**
 * @title Module 2: CSV to PSD
 * @version 1.0
 * @author tlcpineda.projects@gmail.com
 * @description Transfer the contents of the CSV file to corresponding PSD files, ready for manual adjustments.
 */

// #target photoshop

// function main() {
//     var doc = app.activeDocument;
//
//     // 2. Identify CSV location
//     // Path logic: PSD is in "2 TYPESETTING", CSV is in the parent folder
//     var psdFolder = doc.path;
//     var parentFolder = psdFolder.parent;
//     var csvFile = new File(parentFolder + "/translations.csv");
//
//     if (!csvFile.exists) {
//         // Log error to a file if needed, but don't use 'alert'
//         return;
//     }
//
//     // 3. Read CSV Content
//     csvFile.open('r');
//     csvFile.encoding = "UTF-8";
//     var content = csvFile.read();
//     csvFile.close();
//
//     var lines = content.split(/\r\n|\n/);
//
//     // 4. Extract Page ID from PSD Filename (Last 2 digits before extension)
//     // Matches your naming: MyMangaTitle_..._05.psd
//     var docName = doc.name.split('.')[0];
//     var pageID = docName.substring(docName.length - 2);
//
//     // 5. Process CSV Lines
//     for (var i = 1; i < lines.length; i++) {
//         if (lines[i] == "") continue;
//
//         var columns = parseCSVLine(lines[i]);
//         var csvPageNum = columns[0].substring(0, 2); // Get "05" from "05X"
//
//         // Only process if CSV row matches current PSD page
//         if (csvPageNum === pageID) {
//             var x0 = parseFloat(columns[1]);
//             var y0 = parseFloat(columns[2]);
//             var w_norm = parseFloat(columns[4]);
//             var h_norm = parseFloat(columns[5]);
//             var text = columns[6].replace(/ <>/g, "\r");
//
//             createParagraphText(doc, text, x0, y0, w_norm, h_norm);
//         }
//     }
// }


function main() {
    var doc = app.activeDocument;
    var doc_name = doc.name;
    var doc_path = doc.path;
    var parent_folder = doc_path.parent;
    var csv_file = new File(parent_folder + '/translations.csv');

    // Fetch CSV file contents.
    if (!csv_file.exists) return;    // Early termination if CSV file containing translations is not found.

    csv_file.open('r');
    csv_file.encoding = 'UTF-8';

    var csv_str = csv_file.read();
    var csv_arr = parse_csv(csv_str);

    // Extract page marker from name of doc.
    var match = doc_name.match(/(\d{2}x)\.psd$/i);  // Get the page marker, just before the extension name.
    var page_mark = match && match.length > 1 ? match[1] : null;

    if (page_mark === null) return; // Early termination if page_mark on filename is not found.

    // Slice csv_arr for elements with matching page marker, before transfer text to currently open file.
    var doc_data = [];

    for (var i=0; i<csv_arr.length; i++) {
        if (csv_arr[i][0].toUpperCase() === page_mark) doc_data.push(csv_arr[i]);
    }

    for (var j=0; j<doc_data.length; j++) {
        var row = doc_data[j];

        transfer_text(doc, row[1], row[2], row[3], row[4], row[5]);
    }
}


/**
 * Transfer the contents of the line from the CSV to the PSD file.
 * @param {Object} doc The currently open PSD file
 * @param {float} x0_norm x-coordinate of the text box, normalised to the width of the source PDF file.
 * @param {float} y0_norm y-coordinate of the text box, normalised to the height of the source PDF file.
 * @param {float} w_norm width of the text box, normalised to the width of the source PDF file.
 * @param {float} h_norm height of the text box, normalised to the height of the source PDF file.
 * @param {string} contents The contents of the text annotation from the PDF file.
 */
function transfer_text(doc, x0_norm, y0_norm, w_norm, h_norm, contents) {
    var text_group_name = "TEXT";
    var text_group = null;

    // Find Group with "TEXT" (case insensitive) in the name; otherwise create Group.
    for (var i=0; i<doc.layerSets.length; i++) {
        if (doc.layerSets[i].name.toUpperCase().indexOf(text_group_name) !== -1) {
            text_group = doc.layerSets[i]
            break;
        }
    }

    if (text_group === null) {
        text_group = doc.layerSets.add();
        text_group.name = text_group_name;
    }

    // Create text layer within "TEXT" group.
    var new_layer = text_group.artLayers.add();

    new_layer.kind = LayerKind.TEXT;

    var text_layer = new_layer.textItem;

    text_layer.kind = TextType.PARAGRAPHTEXT;

    var w_doc = doc.width.as('px');
    var h_doc = doc.height.as('px');

    text_layer.width = w_norm * w_doc;
    text_layer.height = h_norm * h_doc;
    text_layer.position = [x0_norm * w_doc, y0_norm * h_doc];
    text_layer.contents = contents;
    text_layer.justification = Justification.CENTER;
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