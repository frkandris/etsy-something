set -e
cd /Users/p.tothandras/Code/etsy-something
export OPENAI_API_KEY=$(cat /private/tmp/claude-501/-Users-p-tothandras-Code-etsy-something/4484a596-0d9b-4f0f-8626-733b39385721/scratchpad/.openai_key)
OUT=product/candidates
mkdir -p $OUT
COMMON="Built entirely from nested MELTING, DRIPPING organic shapes - thick poured paint in flat layers, each level an irregular blob with rounded lobes and soft drips running downward, nesting inside the one behind it. NO border, NO ornament: the area around the subject is one flat empty background level filling at least a third of the picture. Few, LARGE, simple, bold shapes - poster art, not fine detail. Leave a clear margin, nothing touching the edge."
gen () { .venv/bin/python product/pipeline/00_generate.py --subject-text "$2 $COMMON" --name "$1" --levels 7 --out $OUT 2>&1 | grep KB; }
gen 01-german-shepherd "A German Shepherd dog head seen straight on, upright ears, alert eyes."
gen 02-peeking-cat     "A cute cat peeking over a horizontal ledge with both front paws hooked over it, big round eyes, seen straight on."
gen 03-wolf            "A wolf head seen straight on, ruff of fur flaring outward, intense eyes."
gen 04-number-five     "A large numeral 5, bold and rounded, filling the centre of the picture."
gen 05-butterfly       "A butterfly with wings spread wide and symmetrical, seen from above."
gen 06-horse           "A horse head in three-quarter view with a flowing mane sweeping backward."
gen 07-elephant        "An elephant head seen straight on, large ears fanned out, trunk curling down."
gen 08-giraffe         "A giraffe head and neck seen straight on, two ossicones on top, long eyelashes."
gen 09-fox             "A fox head seen straight on, pointed ears, narrow muzzle, bushy cheek fur."
gen 10-highland-cow    "A highland cow head seen straight on, long shaggy fringe over the eyes, wide curved horns."
ls -la $OUT | tail -12
