import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    maxEventsToPrint = cms.untracked.int32(0),
    comEnergy = cms.double(13000.0),
    ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2014_NOLONGLIFE.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt_2014.pdl'),
            list_forced_decays = cms.vstring(
                'MyB+',
                'MyB-',
            ),
            operates_on_particles = cms.vint32(521),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyLepD0         D0
Alias      MyLepanti-D0    anti-D0
Alias      MyLepD*0        D*0
Alias      MyLepanti-D*0   anti-D*0
Alias      MyD0            D0
Alias      Myanti-D0       anti-D0
Alias      MyD*-           D*-
Alias      MyD*+           D*+
Alias      MyLepTau+       tau+
Alias      MyLepTau-       tau-
Alias      MyLepD_s*+      D_s*+
Alias      MyLepD_s*-      D_s*-
Alias      MyLepD_s+       D_s+
Alias      MyLepD_s-       D_s-
Alias      Myanti-D_2*0    anti-D_2*0
Alias      MyD_2*0         D_2*0
Alias      MyB+            B+
Alias      MyB-            B-

ChargeConj MyLepD0        MyLepanti-D0
ChargeConj MyLepD*0       MyLepanti-D*0
ChargeConj MyD0           Myanti-D0
ChargeConj MyD*-          MyD*+
ChargeConj MyLepTau+      MyLepTau-
ChargeConj MyLepD_s+      MyLepD_s-
ChargeConj MyLepD_s*+     MyLepD_s*-
ChargeConj MyD_2*0        Myanti-D_2*0
ChargeConj MyB+           MyB-

Decay MyD0
1.000       K-  pi+           PHSP;
Enddecay
CDecay Myanti-D0

Decay MyD*-
1.000       Myanti-D0 pi-     VSS;
Enddecay
CDecay MyD*+

Decay Myanti-D_2*0
0.2090    MyD*- pi+                        TVS_PWAVE  0.0 0.0 1.0 0.0 0.0 0.0;
Enddecay
CDecay MyD_2*0

Decay MyLepTau+
1.000      mu+  nu_mu   anti-nu_tau         TAULNUNU;
Enddecay
CDecay MyLepTau-

Decay MyLepD_s+
0.02390 phi        mu+     nu_mu   PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.02320 eta        mu+     nu_mu   PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00800 eta'       mu+     nu_mu   PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00340 anti-K0    mu+     nu_mu   PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00215 anti-K*0   mu+     nu_mu   PHOTOS  ISGW2; #[Reconstructed PDG2011]
0.00931 MyLepTau+          nu_tau  PHOTOS  SLN;   # PDG, includes tau -> mu nunu
0.00549 mu+                nu_mu   PHOTOS  SLN;   # PDG
Enddecay
CDecay MyLepD_s-

Decay MyLepD_s*+
0.9350 MyLepD_s+    gamma          VSP_PWAVE; #[Reconstructed PDG2011]
0.0580 MyLepD_s+    pi0            VSS; #[Reconstructed PDG2011]
0.0067 MyLepD_s+    e+         e-  PHSP; #[Reconstructed PDG2011]
Enddecay
CDecay MyLepD_s*-

Decay MyB+
0.0042   Myanti-D_2*0  MyLepD_s+    STS;
0.0040   Myanti-D_2*0  MyLepD_s*+  PHSP;
Enddecay
CDecay MyB-

End
"""
            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring(
            'SoftQCD:nonDiffractive = on',
            'PTFilter:filter = on', # this turn on the filter
            'PTFilter:quarkToFilter = 5', # PDG id of q quark
            'PTFilter:scaleToFilter = 5.0',
	),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)

###### Filters ##########
bmesonFilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(999999),
    MinEta = cms.untracked.double(-999999),
    MinPt = cms.untracked.double(0),
    ParticleID = cms.untracked.int32(521) # B+/-
)

tagfilter = cms.EDFilter("PythiaFilter",
    MaxEta = cms.untracked.double(1.6),
    MinEta = cms.untracked.double(-1.6),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13), # mu
)

D0filter = cms.EDFilter(
    "PythiaDauVFilter",
    ChargeConjugation  = cms.untracked.bool(True),
    ParticleID         = cms.untracked.int32(-421),
    MotherID           = cms.untracked.int32(-413),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(321, -211),
    MinPt              = cms.untracked.vdouble(0.3, 0.3),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

ProductionFilterSequence = cms.Sequence(generator + bmesonFilter + tagfilter + D0filter)
