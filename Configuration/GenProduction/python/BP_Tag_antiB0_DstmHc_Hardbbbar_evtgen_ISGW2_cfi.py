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
            # operates_on_particles = cms.vint32(-511),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
#
# This is the decay file for the decay B- -> Dst Hc (-> mu)
# Br will be normalized to D+ -> mu+X
#
yesPhotos
#
Alias myLepD0 D0
Decay myLepD0
0.03410     K-      mu+     nu_mu                           PHOTOS  ISGW2; # PDG2019
0.01890     K*-     mu+     nu_mu                           PHOTOS  ISGW2; # PDG2019
0.00260     pi-     mu+     nu_mu                           PHOTOS  ISGW2; # PDG2019
0.00177     rho-    mu+     nu_mu                           PHOTOS  ISGW2; # PDG2019 for electron
Enddecay
# Inclusive Br from PDG2020 D0 -> mu +X = 6.8 +/- 0.6%
#
#
Alias myLepD+ D+
Decay myLepD+
0.08760     anti-K0   mu+     nu_mu                         PHOTOS  ISGW2; # PDG2020
0.05270     anti-K*0  mu+     nu_mu                         PHOTOS  ISGW2; # PDG2020
0.03560     K- pi+    mu+     nu_mu                         PHOTOS   PHSP; # PDG2020
Enddecay
## Inclusive Br from PDG 2020 = 17.6 %
#
#
Alias myLepD*+ D*+
Decay myLepD*+
0.26160     myLepD0  pi+                                    VSS; #0.677*6.8/17.6
0.33300     myLepD+  pi0                                    VSS;
Enddecay
# Br sum = 0.5946
#
#
#
#
#
##########################################
#           D*- -> D0(->Kpi) pi
##########################################
#
Alias      Myanti-D0   anti-D0
Decay Myanti-D0
1.000      K+  pi-                PHSP;
Enddecay
#
Alias     MyD*-    D*-
Decay MyD*-
1.000      Myanti-D0 pi-          VSS;
Enddecay
#
#
#
#
#
#
#
##########################################
#           anti-B0 -> D*- Hc
##########################################
#
Decay anti-B0
0.00320     MyD*-         myLepD+         anti-K0                      PHSP; # [Reconstructed PDG2020], gamma 172
0.00482     MyD*-         myLepD*+        anti-K0                      PHSP; # [Reconstructed PDG2020]   #  0.0081 * 0.5946, gamma 173
######## 0.00370     MyD*-         myLepD*+        K*0                       PHSP; # Not reported in PDG, neglected
Enddecay
# Sum of weighted Br = 0.00802
End
"""
                                            )
        ),
        parameterSets = cms.vstring('EvtGen130')
    ),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        processParameters = cms.vstring('HardQCD:hardbbbar = on'),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'processParameters',
                                    )
    )
)


###### Filters ##########
mufilter = cms.EDFilter("PythiaFilter",
    MaxEta     = cms.untracked.double(1.6),
    MinEta     = cms.untracked.double(-1.6),
    MinPt      = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13),
)

DstFilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(-413),
    MotherID           = cms.untracked.int32(-511),
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-421, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.25),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

antiD0Filter = cms.EDFilter(
    "PythiaDauVFilter",
    ChargeConjugation  = cms.untracked.bool(False),
    ParticleID         = cms.untracked.int32(-421),
    MotherID           = cms.untracked.int32(-413),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(321, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.5),
    MinEta             = cms.untracked.vdouble(-2.5, -2.5),
    MaxEta             = cms.untracked.vdouble( 2.5, 2.5)
)

ProductionFilterSequence = cms.Sequence(generator + mufilter + DstFilter + antiD0Filter)
