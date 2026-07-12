// This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['kaitai-struct/KaitaiStream'], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('kaitai-struct/KaitaiStream'));
  } else {
    root.Th09 = factory(root.KaitaiStream);
  }
}(typeof self !== 'undefined' ? self : this, function (KaitaiStream) {
var Th09 = (function() {
  function Th09(_io, _parent, _root) {
    this._io = _io;
    this._parent = _parent;
    this._root = _root || this;

    this._read();
  }
  Th09.prototype._read = function() {
    this.fileHeader = new FileHeader(this._io, this, this._root);
    this.header = new Header(this._io, this, this._root);
    this.stages = [];
    for (var i = 0; i < 20; i++) {
      this.stages.push(new StageInstance(this._io, this, this._root, i));
    }
  }

  var Stage = Th09.Stage = (function() {
    function Stage(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Stage.prototype._read = function() {
      this.score = this._io.readU4le();
      this.pair = this._io.readU2le();
      this.shot = this._io.readU1();
      this.ai = this._io.readBitsIntBe(1) != 0;
      this._io.alignToByte();
      this.lives = this._io.readU1();
      this.unknown = this._io.readU1();
    }

    return Stage;
  })();

  /**
   * blank type
   */

  var Dummy = Th09.Dummy = (function() {
    function Dummy(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Dummy.prototype._read = function() {
    }

    return Dummy;
  })();

  var StageInstance = Th09.StageInstance = (function() {
    function StageInstance(_io, _parent, _root, idx) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;
      this.idx = idx;

      this._read();
    }
    StageInstance.prototype._read = function() {
    }
    Object.defineProperty(StageInstance.prototype, 'body', {
      get: function() {
        if (this._m_body !== undefined)
          return this._m_body;
        var _pos = this._io.pos;
        this._io.seek(this._parent.fileHeader.stageOffsets[this.idx]);
        switch (this._parent.fileHeader.stageOffsets[this.idx]) {
        case 0:
          this._m_body = new Dummy(this._io, this, this._root);
          break;
        default:
          this._m_body = new Stage(this._io, this, this._root);
          break;
        }
        this._io.seek(_pos);
        return this._m_body;
      }
    });

    return StageInstance;
  })();

  var Header = Th09.Header = (function() {
    function Header(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    Header.prototype._read = function() {
      this.unknown1 = this._io.readU4le();
      this.date = KaitaiStream.bytesToStr(KaitaiStream.bytesTerminate(this._io.readBytes(10), 0, false), "ASCII");
      this.name = KaitaiStream.bytesToStr(KaitaiStream.bytesTerminate(this._io.readBytes(9), 0, false), "SJIS");
      this.difficulty = this._io.readU1();
    }

    return Header;
  })();

  var FileHeader = Th09.FileHeader = (function() {
    function FileHeader(_io, _parent, _root) {
      this._io = _io;
      this._parent = _parent;
      this._root = _root || this;

      this._read();
    }
    FileHeader.prototype._read = function() {
      this.magic = this._io.readBytes(4);
      if (!((KaitaiStream.byteArrayCompare(this.magic, [84, 57, 82, 80]) == 0))) {
        throw new KaitaiStream.ValidationNotEqualError([84, 57, 82, 80], this.magic, this._io, "/types/file_header/seq/0");
      }
      this.version = this._io.readU2le();
      this.unknown1 = this._io.readBytes(6);
      this.compSize = this._io.readU4le();
      this.unknown2 = this._io.readU4le();
      this.key = this._io.readU1();
      this.unknown3 = this._io.readBytes(7);
      this.decompSize = this._io.readU4le();
      this.stageOffsets = [];
      for (var i = 0; i < 20; i++) {
        this.stageOffsets.push(this._io.readU4le());
      }
      this.unknownOffsets = [];
      for (var i = 0; i < 20; i++) {
        this.unknownOffsets.push(this._io.readU4le());
      }
    }

    /**
     * These look like more stage offsets, but I have no idea what they do or what they're for, and they're causing EOF errors when trying to parse them as stages sometimes, so I've chosen to ignore them
     */

    return FileHeader;
  })();

  return Th09;
})();
return Th09;
}));
