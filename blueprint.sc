__config()->{
	'stay_loaded' : true,
	'scope'->'global',
	'commands' -> {
		' ' -> '__print_default',
		'info' -> '_palette',
		'save <name>' ->'saveAs',
		'load <savedblueprint>' -> 'loadAs',
		'loadZip <zip> <filename>' -> 'loadfromZip'
		},
	'arguments' -> {
		'savedblueprint' -> {'type' -> 'term',
			 'suggester'->_(args) -> (
                        list_files('','nbt')
      				 ),
			},
		'name' -> {'type' -> 'term'},
		'zip' -> {'type' -> 'term'},
		'filename' -> {'type' -> 'term'},
		}
};

global_save_limit = 50;

__print_default()->(
	print(player(), '/blueprint info -> prints required materials');
	print(player(), '/blueprint save <name> -> saves current blueprint data as <name>, OP only');
	print(player(), '/blueprint load <name> -> loads blueprint data into current blueprint, overrides data' );
);

_is_empty()->(
	player()~'holds':0 == 'bitsandchisels:blueprint' && player()~'holds':2 == null
);
_is_not_empty()->(
	player()~'holds':0 == 'bitsandchisels:blueprint' && player()~'holds':2 != null
);
_holds()->(
	player()~'holds':0 == 'bitsandchisels:blueprint'
);
_palette()->(
	if(_is_empty(), print(player(), 'No blueprint is being holded'); return());
	palette = parse_nbt(player()~'holds':2:'blueprint.palette[]'); //lists of nbts
	bits = player()~'holds':2:'blueprint.bits_v2[]';
	hist = {};
	if(bits == null, return(null));
	i = 0;
	for(range(4096),
		hist : ((bits : (2*_+1))*256 + (bits : (2*_))) += 1
	);
	for(hist,
		name = palette:_:'Name';
		count = hist:_;
		print(player(), 'Bits : '+name+ ' '+count);
	)
);
getTime()->(
	t = convert_date(unix_time());
	''+ t:0 + t:1 + t:2
);

_check_save_limit()->(
	if (player()~'permission_level'>= 3, return(true));
	for(list_files('','nbt'),
		_~(player()~'name')
	) < global_save_limit
);

saveAs(fileName)->(
	//if(player()~'permission_level'<3, print(player(), 'Not enough permission level : ask for gm');return());
	if(!_check_save_limit(), print('Too many saved blueprints : ask for gm');return());
	if(_is_not_empty(),
		data = player()~'holds':2;
		write_file((player()~'name')+getTime()+fileName, 'nbt', data);
	);
	print(player(), 'Saved blueprint as '+fileName)
);

loadAs(fileName)->(
	if(!_holds(),  print(player(), 'No blueprint is being holded');return());
	file = read_file(fileName, 'nbt');
	if(file == null, print(player(), 'No file exists'); return());
	slot = player()~'selected_slot';
	inventory_set(player(), slot, 1, 'bitsandchisels:blueprint', file);
	print(player(), 'Successfully loaded blueprint')
);
loadfromZip(zipName, fileName)->(
	if(!_holds(),  print(player(), 'No blueprint is being holded');return());
	file = read_file(zipName + '.zip/'+ fileName, 'nbt');
	if(file == null, print(player(), 'No file exists'); return());
	slot = player()~'selected_slot';
	inventory_set(player(), slot, 1, 'bitsandchisels:blueprint', file);
	print(player(), 'Successfully loaded blueprint')
);
loadRawAndSet(fileName, pos)->(
	file = read_file(fileName, 'nbt');
	nbt = file:'blueprint';
	set(pos, 'bitsandchisels:bits_block', ['waterlogged', 'false'], nbt)
);

getFilesContains(path, delimeter)->(
	lf = list_files(path, 'nbt');
	ll = [];
	for(lf, if(_~delimeter,put(ll, null, _) ));
	ll
);

processString(string)->(
	a = split('/',string);
	a = get(a, length(a)-1);
	a =replace(a, 'a', '_');
	a =replace(a, 'b', '_');
	s = split('_',a);
	print(s);
	[number(get(s,1)), number(get(s,2)), number(get(s,3))]
);

pasteFrom(path, delimeter, origin)->(
	for(getFilesContains(path, delimeter),
		fileName = _;
		posO = processString(_) + origin;
		loadRawAndSet(fileName, posO);	
		sleep(50);
	);
	
)