import requests

response = requests.post("https://localhost:35103/notesverse/make_graph", json={"name": "Biology", "text": """
Biological Molecules> Proteins, Nucleic Acids, Carbohydrates, Fats
Proteins: made of> Polypeptides
Polypeptides: made of> Amino Acids
Amino Acids: link together by> Peptide Bonds
Proteins> Enzymes, Antibodies, Hormones
Enzymes: biological catalysts
Proteins: breaks down to> Carbon, Hydrogen, Oxygen, Nitrogen
                       
Carbohydrates> Monosaccharides, Disaccharides, Polysaccharides
Monosaccharides> Glucose, Fructose, Galactose
Disaccharides> Sucrose, Lactose, Maltose
Polysaccharides> Starch, Glycogen, Cellulose
Monosaccharides: link together by> Glycosidic Bonds
Disaccharides: made of> Monosaccharides
Polysaccharides: made of> Monosaccharides
Monosaccharides: single
Disaccharides: double
Polysaccharides: complex
Carbohydrates: short-term energy
Carbohydrates: breaks down to> Carbon, Hydrogen, Oxygen
Glucose: main energy source
Fructose: fruit sugar
Lactose: milk sugar
Maltose: malt sugar
Sucrose: table sugar
Starch: energy storage in plants
Glycogen: energy storage in animals
Cellulose: structural component in plants
Glycogen: stored in> Liver
                       
Fats: long-term energy, insulation, protection
Fats: more energy than> Carbohydrates
Fats: made of> Glycerol, Fatty Acids
Fats> Triglycerides, Phospholipids, Steroids
Fats: can be> Saturated, Unsaturated
Fatty Acids: double bonds> Unsaturated
Fatty Acids: no double bonds> Saturated
Fatty Acids: hydrophillic
Glycerol: hydrophobic
Fats: Amphipathic
Fats: breaks down to> Carbon, Hydrogen, Oxygen
Saturated: straight
Unsaturated: bent
                       
Nucleic Acids> DNA, RNA
Nucleic Acids: made of> Nucleotides
Nucleotides: made of> Monosaccharides, Phosphate Group, Nitrogenous Bases
DNA: double stranded
RNA: single stranded
DNA: deoxyribose
RNA: ribose
DNA: stores genetic information
RNA: turns genetic information into proteins
Nitrogenous Bases> Adenine, Thymine, Cytosine, Guanine, Uracil
DNA: bases> Adenine, Thymine, Cytosine, Guanine
RNA: bases> Adenine, Uracil, Cytosine, Guanine
Adenine: pairs with> Thymine, Uracil
Cytosine: pairs with> Guanine
Food Tests> Benedict's Test, Iodine Test, Biuret Test, Ethanol Emulsion Test
Benedict's Test: tests for> Reducing Sugars
Reducing Sugars: Glucose, Fructose, Galactose
Iodine Test: tests for> Starch
Biuret Test: tests for> Proteins
Ethanol Emulsion Test: tests for> Fats
Benedict's Test: blue to brick red
Iodine Test: yellow to blue-black
Biuret Test: blue to purple
Ethanol Emulsion Test: clear to cloudy white
      """})

print(response.text)  # This will print the generated HTML for the graph