async function recognize(_base64, lang, options) {
    console.log(`[EasyOCR Plugin] Starting recognition with lang: ${lang}`);

    const { utils } = options;
    const { run, cacheDir, pluginDir } = utils;

    const imagePath = `${cacheDir}/pot_screenshot_cut.png`;
    console.log(`[EasyOCR Plugin] Using image: ${imagePath}`);

    console.log(`[EasyOCR Plugin] Running python ocr.py...`);
    let result = await run('python', [
        `${pluginDir}/ocr.py`,
        imagePath,
        lang
    ]);

    console.log(`[EasyOCR Plugin] Python exited with status: ${result.status}`);
    console.log(`[EasyOCR Plugin] Full stdout: ${result.stdout}`);

    if (result.status === 0) {
        let out = result.stdout;
        out = out.split("OCR init completed.");
        if (out.length > 1) {
            out = out[1].trim();
        } else {
            out = out[0].trim();
        }
        // 加這行：取 split 後第一行（防多餘 print）
        out = out.split('\n')[0].trim();
        console.log(`[EasyOCR Plugin] Extracted for parse: ${out}`);

        let json;
        try {
            json = JSON.parse(out);
            console.log(`[EasyOCR Plugin] Parsed JSON data length: ${json.data.length}`);
        } catch (parseErr) {
            console.error(`[EasyOCR Plugin] JSON parse failed on: ${out} | Error: ${parseErr}`);
            throw parseErr;
        }
        let target = "";
        for (let line of json.data) {
            target += `${line.text}\n`;
        }
        console.log(`[EasyOCR Plugin] Final text (length: ${target.length}): ${target.substring(0, 100)}...`);
        return target.trim();
    } else {
        console.error(`[EasyOCR Plugin] Python error: ${result.stderr}`);
        throw Error(result.stderr);
    }
}