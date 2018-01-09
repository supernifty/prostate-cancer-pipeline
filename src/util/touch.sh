
# hp dataset
#S="CMHS51 CMHS52 CMHS53 CMHS54 CMHS55 CMHS64 CMHS65 CMHS66 CMHS67 CMHS68 CMHS69 CMHS70 CMHS71"

# train dataset
#S="CMHS100 CMHS113 CMHS116 CMHS167 CMHS168 CMHS169 CMHS170 CMHS173 CMHS174 CMHS178 CMHS179 CMHS187 CMHS188 CMHS193 CMHS194 CMHS195 CMHS196 CMHS197 CMHS198 CMHS199 CMHS200 CMHS203 CMHS204 CMHS205 CMHS206 CMHS207 CMHS208 CMHS209 CMHS210 CMHS211 CMHS212 CMHS215 CMHS216 CMHS219 CMHS220 CMHS221 CMHS222 CMHS227 CMHS228 CMHS229 CMHS230 CMHS236 CMHS237 CMHS238 CMHS239 CMHS240 CMHS241 CMHS242 CMHS243 CMHS248 CMHS249 CMHS256 CMHS257 CMHS258 CMHS259 CMHS265 CMHS266 CMHS267 CMHS268 CMHS269 CMHS270 CMHS271 CMHS272 CMHS277 CMHS278 CMHS279 CMHS280 CMHS281 CMHS282 CMHS285 CMHS286 CMHS287 CMHS288 CMHS291 CMHS292 CMHS293 CMHS294 CMHS301 CMHS302 CMHS303 CMHS304 CMHS305 CMHS306 CMHS307 CMHS308 CMHS309 CMHS310 CMHS311 CMHS312 CMHS315 CMHS316 CMHS317 CMHS318 CMHS319 CMHS320 CMHS72 CMHS74 CMHS86 CMHS89 CMHS97"

# remain dataset
S="CMHS1 CMHS10 CMHS101 CMHS102 CMHS103 CMHS104 CMHS105 CMHS106 CMHS107 CMHS108 CMHS109 CMHS11 CMHS110 CMHS111 CMHS112 CMHS114 CMHS115 CMHS117 CMHS118 CMHS119 CMHS12 CMHS120 CMHS121 CMHS122 CMHS123 CMHS124 CMHS125 CMHS126 CMHS127 CMHS128 CMHS129 CMHS13 CMHS130 CMHS131 CMHS132 CMHS133 CMHS134 CMHS135 CMHS136 CMHS137 CMHS138 CMHS139 CMHS14 CMHS140 CMHS141 CMHS142 CMHS143 CMHS144 CMHS145 CMHS146 CMHS147 CMHS148 CMHS149 CMHS15 CMHS150 CMHS151 CMHS152 CMHS153 CMHS154 CMHS155 CMHS156 CMHS157 CMHS158 CMHS159 CMHS16 CMHS160 CMHS161 CMHS162 CMHS163 CMHS164 CMHS165 CMHS166 CMHS17 CMHS171 CMHS172 CMHS175 CMHS176 CMHS177 CMHS18 CMHS180 CMHS181 CMHS182 CMHS183 CMHS184 CMHS185 CMHS186 CMHS189 CMHS19 CMHS190 CMHS191 CMHS192 CMHS2 CMHS20 CMHS201 CMHS202 CMHS21 CMHS213 CMHS214 CMHS217 CMHS218 CMHS22 CMHS223 CMHS224 CMHS225 CMHS226 CMHS23 CMHS231 CMHS232 CMHS233 CMHS234 CMHS235 CMHS24 CMHS244 CMHS245 CMHS246 CMHS247 CMHS25 CMHS250 CMHS251 CMHS252 CMHS253 CMHS254 CMHS255 CMHS26 CMHS260 CMHS261 CMHS262 CMHS263 CMHS264 CMHS27 CMHS273 CMHS274 CMHS275 CMHS276 CMHS28 CMHS283 CMHS284 CMHS289 CMHS29 CMHS290 CMHS295 CMHS296 CMHS297 CMHS298 CMHS299 CMHS3 CMHS30 CMHS300 CMHS31 CMHS313 CMHS314 CMHS32 CMHS321 CMHS322 CMHS323 CMHS324 CMHS325 CMHS326 CMHS327 CMHS328 CMHS329 CMHS33 CMHS330 CMHS331 CMHS332 CMHS333 CMHS334 CMHS335 CMHS336 CMHS337 CMHS338 CMHS339 CMHS34 CMHS340 CMHS341 CMHS342 CMHS343 CMHS344 CMHS345 CMHS346 CMHS347 CMHS348 CMHS349 CMHS35 CMHS350 CMHS351 CMHS352 CMHS353 CMHS354 CMHS355 CMHS356 CMHS357 CMHS358 CMHS359 CMHS36 CMHS360 CMHS361 CMHS362 CMHS363 CMHS364 CMHS365 CMHS366 CMHS367 CMHS368 CMHS369 CMHS37 CMHS370 CMHS371 CMHS372 CMHS373 CMHS374 CMHS375 CMHS376 CMHS377 CMHS38 CMHS39 CMHS4 CMHS40 CMHS41 CMHS42 CMHS43 CMHS44 CMHS45 CMHS46 CMHS47 CMHS48 CMHS49 CMHS5 CMHS50 CMHS56 CMHS57 CMHS58 CMHS59 CMHS6 CMHS60 CMHS61 CMHS62 CMHS63 CMHS7 CMHS73 CMHS75 CMHS76 CMHS77 CMHS78 CMHS79 CMHS8 CMHS80 CMHS81 CMHS82 CMHS83 CMHS84 CMHS85 CMHS87 CMHS88 CMHS9 CMHS90 CMHS91 CMHS92 CMHS93 CMHS94 CMHS95 CMHS96 CMHS98 CMHS99"

LIVE=true
#LIVE=false

# bam
for s in $S; do
  f=../out/$s.bam
  if [ -s $f ]; then
    echo "touching $f"
    $LIVE && touch "$f"
  else
    echo "creating empty $f"
    $LIVE && touch "$f"
  fi
done

# validation
for s in $S; do
  f=../out/$s.validation
  if [ -s $f ]; then
    echo "touching $f"
    $LIVE && touch "$f"
  else
    echo "missing $f: removing"
    $LIVE && rm -f "$f"
  fi
done

# mapped.bam
for s in $S; do
  f=../out/$s.mapped.bam
  if [ -s $f ]; then
    echo "touching $f" # mapped is present
    $LIVE && touch "$f"
  else
    # mapped isn't present
    g=../out/$s.bam
    if [ -s $f ]; then
      # unmapped bam is present, mapped is not
      echo "removing $f"
      $LIVE && rm -f "$f"
    else
      echo "removing $f and $g"
      $LIVE && rm -f "$f" "$g"
    fi
  fi
done

for s in $S; do
  f="../out/$s.wgs.1.1.2/WGS_*.tar.gz"
  #echo "testing $f"
  if compgen -G "$f" > /dev/null; then
    g="../out/$s.wgs.1.1.2/completed.*"
    echo "touching $g"
    $LIVE && touch $g
  else
    g="../out/$s.wgs.1.1.2"
    echo "removing $g"
    $LIVE && rm -rf "$g"
    g="../tmp/wgs-1.1.2-$s"
    echo "removing $g"
    $LIVE && rm -rf "$s"
  fi
done

# fastqc
for s in $S; do
  f="../out/${s}_R1_fastqc"
  #echo "testing $f"
  if [ -s $f ]; then
    echo "touching $f"
    $LIVE && touch "$f"
  fi
  f="../out/${s}_R2_fastqc"
  if [ -s $f ]; then
    echo "touching $f"
    $LIVE && touch "$f"
  fi
done

# genomecov
for s in $S; do
  f="../out/${s}.genomecov.stats"
  #echo "testing $f"
  if [ -s $f ]; then
    echo "touching $f"
    $LIVE && touch "$f"
  fi
done

# picard
for s in $S; do
  f="../out/${s}.picard.stats"
  #echo "testing $f"
  if [ -s $f ]; then
    echo "touching $f"
    $LIVE && touch "$f"
  fi
done

# muse
for s in $S; do
  f="../out/${s}.muse.vcf"
  #echo "testing $f"
  g="../out/${s}.muse.completed"
  if [ -s $f ]; then
    echo "touching $g"
    $LIVE && touch "$g"
  else
    echo "removing $g"
    $LIVE && rm -f "$g"
  fi
done

# platypus
for s in $S; do
  f="../out/${s}.platypus.vcf"
  #echo "testing $f"
  g="../out/${s}.platypus.completed"
  if [ -s $f ]; then
    echo "touching $g"
    $LIVE && touch "$g"
  else
    echo "removing $g"
    $LIVE && rm -f "$g"
  fi
done
# mutect1
for s in $S; do
  f="../out/${s}.mutect1.vcf"
  #echo "testing $f"
  g="../out/${s}.mutect1.completed"
  if [ -s $f ]; then
    echo "touching $g"
    $LIVE && touch "$g"
  else
    echo "removing $g"
    $LIVE && rm -f "$g"
  fi
done
# gridss
for s in $S; do
  f="../out/${s}.gridss.vcf"
  #echo "testing $f"
  g="../out/${s}.gridss.completed"
  if [ -s $f ]; then
    echo "touching $g"
    $LIVE && touch "$g"
  else
    echo "removing $g"
    $LIVE && rm -f "$g"
  fi
done
# varscan
for s in $S; do
  f="../out/${s}.varscan.vcf"
  #echo "testing $f"
  g="../out/${s}.varscan.completed"
  if [ -s $f ]; then
    echo "touching $g"
    $LIVE && touch "$g"
  else
    echo "removing $g"
    $LIVE && rm -f "$g"
  fi
done

echo "now recreate database"
