	

    --[[Mp3 id3 v2.3 tag reader APIC Extract/edit/insert - By WeBuLtR@
     
    Changelog v0.9.0.0:
            - Added function id3.readAPICInfo: Returns available info of the APIC frame and can extract the APIC picture
            - Improved function id3.changeArt: Added PNG support (omits png's CRC), description and much more;
            - Fixed function id3.changeArt: Was deleting the mp3 data if a png image was found and removed unnecessary code
            - Fixed function id3.getArt: Was failing while extracting png files
     
    NOTES:
            - This code won't work with unicode data for now
            - id3.getArt and id3.readAPICInfo functions extract the APIC picture file in different ways
    ]]--
    id3 = {};
    id3.version = "0.9.0.0";
    function id3.getV1(mp3)
    --Thnx to: http://psp.scenebeta.com/node/70241
            local name,artist,album,track,genre,year,comment = ""
            local tGenre = {};
            tGenre[0] = "Blues";
            tGenre[1] = "Classic Rock";
            tGenre[2] = "Country";
            tGenre[3] = "Dance";
            tGenre[4] = "Disco";
            tGenre[5] = "Funk";
            tGenre[6] = "Grunge";
            tGenre[7] = "Hip-Hop";
            tGenre[8] = "Jazz";
            tGenre[9] = "Metal";
            tGenre[10] = "New Age";
            tGenre[11] = "Oldies";
            tGenre[12] = "Other";
            tGenre[13] = "Pop";
            tGenre[14] = "R&B";
            tGenre[15] = "Rap";
            tGenre[16] = "Reggae";
            tGenre[17] = "Rock";
            tGenre[18] = "Techno";
            tGenre[19] = "Industrial";
            tGenre[20] = "Alternative";
            tGenre[21] = "Ska";
            tGenre[22] = "Death Metal";
            tGenre[23] = "Pranks";
            tGenre[24] = "Soundtrack";
            tGenre[25] = "Euro-Techno";
            tGenre[26] = "Ambient";
            tGenre[27] = "Trip-Hop";
            tGenre[28] = "Vocal";
            tGenre[29] = "Jazz+Funk";
            tGenre[30] = "Fusion";
            tGenre[31] = "Trance";
            tGenre[32] = "Classical";
            tGenre[33] = "Instrumental";
            tGenre[34] = "Acid";
            tGenre[35] = "House";
            tGenre[36] = "Game";
            tGenre[37] = "Sound Clip";
            tGenre[38] = "Gospel";
            tGenre[39] = "Noise";
            tGenre[40] = "Alternative Rock";
            tGenre[41] = "Bass";
            tGenre[43] = "Punk";
            tGenre[44] = "Space";
            tGenre[45] = "Meditative";
            tGenre[46] = "Instrumental Pop";
            tGenre[47] = "Instrumental Rock";
            tGenre[48] = "Ethnic";
            tGenre[49] = "Gothic";
            tGenre[50] = "Darkwave";
            tGenre[51] = "Techno-Industrial";
            tGenre[52] = "Electronic";
            tGenre[53] = "Pop-Folk";
            tGenre[54] = "Eurodance";
            tGenre[55] = "Dream";
            tGenre[56] = "Southern Rock";
            tGenre[57] = "Comedy";
            tGenre[58] = "Cult";
            tGenre[59] = "Gangsta";
            tGenre[60] = "Top 40";
            tGenre[61] = "Christian Rap";
            tGenre[62] = "Pop/Funk";
            tGenre[63] = "Jungle";
            tGenre[64] = "Native US";
            tGenre[65] = "Cabaret";
            tGenre[66] = "New Wave";
            tGenre[67] = "Psychadelic";
            tGenre[68] = "Rave";
            tGenre[69] = "Showtunes";
            tGenre[70] = "Trailer";
            tGenre[71] = "Lo-Fi";
            tGenre[72] = "Tribal";
            tGenre[73] = "Acid Punk";
            tGenre[74] = "Acid Jazz";
            tGenre[75] = "Polka";
            tGenre[76] = "Retro";
            tGenre[77] = "Musical";
            tGenre[78] = "Rock & Roll";
            tGenre[79] = "Hard Rock";
            tGenre[80] = "Folk";
            tGenre[81] = "Folk-Rock";
            tGenre[82] = "National Folk";
            tGenre[83] = "Swing";
            tGenre[84] = "Fast Fusion";
            tGenre[85] = "Bebob";
            tGenre[86] = "Latin";
            tGenre[87] = "Revival";
            tGenre[88] = "Celtic";
            tGenre[89] = "Bluegrass";
            tGenre[90] = "Avantgarde";
            tGenre[91] = "Gothic Rock";
            tGenre[92] = "Progressive Rock";
            tGenre[93] = "Psychedelic Rock";
            tGenre[94] = "Symphonic Rock";
            tGenre[95] = "Slow Rock";
            tGenre[96] = "Big Band";
            tGenre[97] = "Chorus";
            tGenre[98] = "Easy Listening";
            tGenre[99] = "Acoustic 100 - Humour";
            tGenre[101] = "Speech";
            tGenre[102] = "Chanson";
            tGenre[103] = "Opera";
            tGenre[104] = "Chamber Music";
            tGenre[105] = "Sonata";
            tGenre[106] = "Symphony";
            tGenre[107] = "Booty Bass";
            tGenre[108] = "Primus";
            tGenre[109] = "Porn Groove";
            tGenre[110] = "Satire";
            tGenre[111] = "Slow Jam";
            tGenre[112] = "Club";
            tGenre[113] = "Tango";
            tGenre[114] = "Samba";
            tGenre[115] = "Folklore";
            tGenre[116] = "Ballad";
            tGenre[117] = "Power Ballad";
            tGenre[118] = "Rhytmic Soul";
            tGenre[119] = "Freestyle";
            tGenre[120] = "Duet";
            tGenre[121] = "Punk Rock";
            tGenre[122] = "Drum Solo";
            tGenre[123] = "Acapella";
            tGenre[124] = "Euro-House";
            tGenre[125] = "Dance Hall";
            tGenre[126] = "Goa";
            tGenre[127] = "Drum & Bass";
            tGenre[128] = "Club-House";
            tGenre[129] = "Hardcore";
            tGenre[130] = "Terror";
            tGenre[131] = "Indie";
            tGenre[132] = "BritPop";
            tGenre[133] = "Negerpunk";
            tGenre[134] = "Polsk Punk";
            tGenre[135] = "Beat";
            tGenre[136] = "Christian Gangsta";
            tGenre[137] = "Heavy Metal";
            tGenre[138] = "Black Metal";
            tGenre[139] = "Crossover";
            tGenre[140] = "Contemporary C";
            tGenre[141] = "Christian Rock";
            tGenre[142] = "Merengue";
            tGenre[143] = "Salsa";
            tGenre[144] = "Thrash Metal";
            tGenre[145] = "Anime";
            tGenre[146] = "JPop";
            tGenre[147] = "SynthPop";
            tGenre[255] = "Not defined";
            local fbuf = io.open(mp3,"rb");
            if fbuf then
                    fbuf:seek("end",-128);
                    local tag = fbuf:read(3);
                    if tag == "TAG" then
                            fbuf:seek("end",-125);
                            name = fbuf:read(30);
                            fbuf:seek("end",-95);
                            artist = fbuf:read(30);
                            fbuf:seek("end",-65);
                            album = fbuf:read(30);
                            fbuf:seek("end",-35);
                            year = fbuf:read(4);
                            fbuf:seek("end",-31);
                            comment = fbuf:read(28);
                            fbuf:seek("end",-2);
                            track = string.byte(fbuf:read(1));
                            fbuf:seek("end",-1);
                            genre = tGenre[string.byte(fbuf:read(1))];
                            for i = 1, string.len(name) do
                                    if string.byte(string.sub(name,-1)) == 0 or string.byte(string.sub(name,-1)) == 32 then
                                            name = string.sub(name,1,-2);
                                    end
                            end
                            for i = 1, string.len(artist) do
                                    if string.byte(string.sub(artist,-1)) == 0 or string.byte(string.sub(artist,-1)) == 32 then
                                            artist = string.sub(artist,1,-2);
                                    end
                            end
                            for i = 1, string.len(album) do
                                    if string.byte(string.sub(album,-1)) == 0 or string.byte(string.sub(album,-1)) == 32 then
                                            album = string.sub(album,1,-2);
                                    end
                            end
                    end
                    fbuf:close();
                    return { name = name, artist = artist, album = album, track = track, genre = genre, year = year, comment = comment };
            else
                    return nil;
            end
    end
     
    function id3.getV2(mp3,tag)
    --Thnx to: http://psp.scenebeta.com/node/70241
            local fbuf = io.open(mp3,"rb")
            local ttag = ""
            if fbuf then
                    fbuf:seek("set")
                    local fdata = fbuf:read(100000)
                    fbuf:close()
            end
            if fdata then
                    local fndid = string.find(fdata, tag)
            end
            if fndid then
                    ttag = string.sub(fdata, fndid + 11, fndid + 9 + string.byte(string.sub(fdata, fndid+7, fndid+7)))
                    ttag = string.gsub(ttag, "\0", "")
            end
            return ttag
    end
     
    function id3.getArt(mp3, dest_file)
    --Thnx to: http://psp.scenebeta.com/node/70241
            local fbuf = io.open(mp3,"rb");
            if fbuf then
                    fbuf:seek("set");
                    local fdata = fbuf:read("*a");
                    local fndid = string.find(fdata, "APIC");
                    if fndid then
                            local beg = string.sub(fdata,fndid);
                            if string.find(beg, "JFIF") then
                                    local beg_pos = string.find(beg, "JFIF")-6;
                                    beg = string.sub(beg,beg_pos)
                                    local fin = string.find(beg, string.char(255)..string.char(217));
                                    if fin then
                                            fin = fin + 1;
                                            img = string.sub(beg,1,fin);
                                            fbuf:close()
                                            local file = io.open(dest_file..".jpg","wb");
                                            file:write(img);
                                            file:close();
                                            return true;
                                    else
                                            return nil, "JPG data not found";
                                    end
                            else
                                    local beg_pos = string.find(beg, "‰PNG")
                                    if beg_pos then
                                            beg = string.sub(beg,beg_pos);
                                            local fin = string.find(beg, "IEND")+7;
                                            img = string.sub(beg,1,fin);
                                            fbuf:close();
                                            local file = io.open(dest_file..".png","wb");
                                            file:write(img);
                                            file:close();
                                            return true;
                                    else
                                            return nil, "File format not found";
                                    end
                            end
                    else
                            return nil, "Couldn't find album art image";
                    end
            else
                    return nil, "Couldn't open mp3 file";
            end
    end
     
    function id3.changeArt(mp3, newIMG, desc)
    --[[Insert or replace an APIC header
    boolean id3.changeArt(string MP3File, string ImageFileToInsert, string ImageDescription);
    Thnx to: MEEEEE (WeBuLtR@) lol]]--
            local sImg = (type(newIMG) == "string") and newIMG or "";
            local _,_,mime = sImg:find("%.+(.+)")
            if not mime then
                    return nil, "Invalid IMG";
            else
                    mime = mime:lower();
                    if mime ~= "jpg" and mime ~= "png" and mime ~= "jpeg" then
                            return nil, "Image must be png or jpg";
                    elseif mime == "jpg" then
                            mime = "jpeg";
                    end
            end
            local sF = io.open(mp3, "rb");
            if sF then
                    local data = sF:read("*a");
                    sF:close();
                    if data:sub(1,3) == "ID3" then
                            local tag_size = data:sub(7,10);
                            local n = "";
                            for x in tag_size:gmatch(".") do
                                    local tmp = id3.Hex2Bin(string.format("%02X", x:byte()));
                                    n = n..tmp:sub(2);
                            end
                            local d = string.format("%032s", n);
                            local size = tonumber("0x"..id3.Bin2Hex(d))+10;
                            local id3_data = data:sub(1, size);
                            local apic = string.find(id3_data, "APIC");
                            local img = io.open(newIMG, "rb");
                            if not img then
                                    return nil, "New ART image not found";
                            end
                            local head_data = string.sub(id3_data, 1, 6);
     
                            --APIC Frame
                            local text_encoding = string.char(0);
                            local mime_type = "image/"..mime..string.char(0);
                            local pic_type = string.char(3);--Default: Front cover
                            local description = (type(desc)=="string") and desc:sub(1,63)..string.char(0) or string.char(0);
                            local img_data = img:read("*a");
     
                            --Check png format
                            if mime == "png" then
                                    if img_data:find("IEND") then
                                            local s,_,v = img_data:find("IEND(.+)");
                                            if not v then
                                                    return nil, "Invalid PNG file";
                                            elseif #v > 4 then
                                                    img_data = img_data:sub(1, s+7);
                                            elseif #v < 4 then
                                                    return nil, "Invalid PNG file, must end with 4 bytes after the IEND chunk";
                                            end
                                    end
                            end
     
                            --APIC Header
                            local apic_head = "APIC";
                            local img_size = string.format("%08X", #text_encoding + #mime_type + #pic_type + #description + #img_data);
                            local img_sdata = "";
                            for s in string.gmatch(img_size , "..") do
                                    img_sdata = img_sdata..string.char(tonumber("0x"..s));
                            end
                            local apic_flag = string.char(0,0);
                            img:close();
     
                            --APIC complete tag
                            local apic_data = apic_head..img_sdata..apic_flag..text_encoding..mime_type..pic_type..description..img_data;
                            if apic then
                                    local fin = string.find(id3_data, string.char(255)..string.char(217));
                                    if fin then
                                            fin = fin+1;
                                    elseif string.find(id3_tag, "IEND") then
                                            fin = string.find(id3_data, "IEND")+7;
                                    else
                                            return nil, "Invalid APIC TAG";
                                    end
                                    local prev_data = string.sub(id3_data, 11, apic-1);
                                    local post_data = string.sub(id3_data, fin+1);
                                    local new_adata = prev_data..apic_data..post_data;
                                    local new_size = id3.IntToSynchSafe(#new_adata);
                                    local  sO = io.open(mp3, "wb");
                                    if sO then
                                            sO:write(head_data..new_size..new_adata..string.sub(data, size+1));
                                            sO:close();
                                            return true, "APIC edited";
                                    else
                                            return nil, "Couldn't reopen file";
                                    end
                            else
                                    local post_data = string.sub(id3_data, 11);
                                    local new_adata = apic_data..post_data;
                                    local new_size = id3.IntToSynchSafe(#new_adata);
                                    local  sO = io.open(mp3, "wb");
                                    if sO then
                                            sO:write(head_data..new_size..new_adata..string.sub(data, size+1));
                                            sO:close();
                                            return true, "APIC inserted";
                                    else
                                            return nil, "Couldn't reopen file";
                                    end
                            end
                    else
                            return nil, "ID3 v2 TAG not found";
                    end
            end
    end
     
    function id3.getID3v23Size(mp3file)
    --[[Returns the ID3 v23 TAG Size
    More info: http://www.id3.org/id3v2.3.0]]--
            local sF = io.open(mp3file, "rb");
            if sF then
                    local data = sF:read(10);
                    sF:close();
                    if data:sub(1,3) == "ID3" then
                            local tag_size = data:sub(7,10);
                            local n = "";
                            for x in tag_size:gmatch(".") do
                                    local tmp = id3.Hex2Bin(string.format("%02X", x:byte()));
                                    n = n..tmp:sub(2);
                            end
                            local d = string.format("%032s", n);
                            return tonumber("0x"..id3.Bin2Hex(d))+10;
                    else
                            return nil, "ID3 v2 TAG not found";
                    end
            else
                    return nil, "File not found";
            end
    end
     
    function id3.IntToSynchSafe(integer)
    --[[Returns the integer converted into a SynchSafe (4 bytes) string + the new integer value (just to check) + the hex value;
    More info: http://en.wikipedia.org/wiki/Synchsafe]]--
            assert(type(integer)=="number", "Value must be a number");
            local hex = string.format("%08x",integer);
            local nhex = id3.Hex2Bin(hex);
            local t,i = {},4;
            for x in string.gmatch(nhex, "........") do
                    t[i] = x;
                    i = i-1;
            end
            local newbin, sres, nt= "", "", {};
            for x, y in pairs(t) do
                    local a, c = y:sub(1,x), y:sub(x+1);
                    table.insert(nt, a);
                    newbin = "0"..c..(nt[x-1] or "")..newbin;
            end
            local newhex = id3.Bin2Hex(newbin);
            for sss in string.gmatch(newhex, "..") do
                    sres = sres..string.char(tonumber("0x"..sss));
            end
            return sres, tonumber("0x"..newhex), "0x"..newhex;
    end
     
    function id3.Hex2Bin(s)
    --[[Thanks to Diaelectronics for the hex2bin and bin2hex functions
    More functions and module: http://www.dialectronics.com/Lua/code/BinDecHex.shtml]]--
            local hex2bin = {
                    ["0"] = "0000",
                    ["1"] = "0001",
                    ["2"] = "0010",
                    ["3"] = "0011",
                    ["4"] = "0100",
                    ["5"] = "0101",
                    ["6"] = "0110",
                    ["7"] = "0111",
                    ["8"] = "1000",
                    ["9"] = "1001",
                    ["a"] = "1010",
                    ["b"] = "1011",
                    ["c"] = "1100",
                    ["d"] = "1101",
                    ["e"] = "1110",
                    ["f"] = "1111"
            };
            local ret = ""
            local i = 0
            for i in string.gfind(s, ".") do
                    i = string.lower(i)
                    ret = ret..hex2bin[i]
            end
            return ret
    end
     
    function id3.Bin2Hex(s)
            local bin2hex = {
                    ["0000"] = "0",
                    ["0001"] = "1",
                    ["0010"] = "2",
                    ["0011"] = "3",
                    ["0100"] = "4",
                    ["0101"] = "5",
                    ["0110"] = "6",
                    ["0111"] = "7",
                    ["1000"] = "8",
                    ["1001"] = "9",
                    ["1010"] = "A",
                    ["1011"] = "B",
                    ["1100"] = "C",
                    ["1101"] = "D",
                    ["1110"] = "E",
                    ["1111"] = "F"
            };
            local l = 0
            local h = ""
            local b = ""
            local rem
            l = string.len(s)
            rem = l % 4
            l = l-1
            h = ""
            if (rem > 0) then
                    s = string.rep("0", 4 - rem)..s
            end
            for i = 1, l, 4 do
                    b = string.sub(s, i, i+3);
                    h = h..bin2hex[b];
            end
            return h;
    end
    function id3.readAPICInfo(mp3, writeAPIC)
    --[[Reads the available info of the APIC frame
    table id3.readAPICInfo(string MP3File, boolean WriteImageFileToTempFile);
    Thnx to MEEEEE (WeBuLtR@) lol]]--
            local tTypes = {};
            tTypes[0] = "Other"
            tTypes[1] = "Icon";--32x32px file icon (PNG only)
            tTypes[2] = "Other icon file";
            tTypes[3] = "Front cover";
            tTypes[4] = "Back conver";
            tTypes[5] = "Leaflet";
            tTypes[6] = "Media";
            tTypes[7] = "Lead artist";
            tTypes[8] = "Artist";
            tTypes[9] = "Conductor";
            tTypes[10] = "Band";
            tTypes[11] = "Composer";
            tTypes[12] = "Lyricist";
            tTypes[13] = "Recording location";
            tTypes[14] = "During recording";
            tTypes[15] = "During performance";
            tTypes[16] = "Video capture";
            tTypes[17] = "Bright colored fish";
            tTypes[18] = "Illustration";
            tTypes[19] = "Band logotype";
            tTypes[20] = "Publisher logotype";
            local wa = (type(writeAPIC)=="boolean") and writeAPIC or false;
            local sF = io.open(mp3, "rb");
            if sF then
                    local sData = sF:read("*a");
                    sF:close();
                    if sData then
                            --APIC HEADER
                            local start = sData:find("APIC");
                            if start then
                                    local sized = sData:sub(start+4, start+7);
                                    local size = "";
                                    for x in sized:gmatch(".") do
                                            size = size..string.format("%X", x:byte());
                                    end
                                    size = tonumber("0x"..size);
                                    local flags = sData:sub(start+8, start+9);
     
                                    --APIC FRAME
                                    local text_encoding = sData:sub(start+10, start+10);
                                    local mimee = sData:find("%z", start+11);
                                    local mime = sData:sub(start+11, mimee-1);
                                    local pic_type = string.byte(sData:sub(mimee+1, mimee+1));
                                    local desc_end = sData:find("%z", mimee+2);
                                    local description = sData:sub(mimee+2, desc_end-1);
                                    description = (#description == 0) and "" or description
                                    local pic_data = sData:sub(desc_end+1, desc_end+1+(size-(1+#mime+1+1+#description+2)));
                                    if wa then
                                            local f = io.open("temp."..mime, "wb");
                                            if f then
                                                    f:write(pic_data);
                                                    f:close();
                                            end
                                    end
                                    return {APICFrameSize = size, ImageSize=#pic_data, MimeType=mime, PictureType=tTypes[pic_type], description=description};
                            else
                                    return nil, "APIC header not found";
                            end
                    end
            end
    end
     

