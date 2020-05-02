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
            operates_on_particles = cms.vint32(511),
            convertPythiaCodes = cms.untracked.bool(False),
            user_decay_embedded= cms.vstring(
"""
Alias      MyD0   D0
Alias      Myanti-D0   anti-D0
ChargeConj MyD0   Myanti-D0
#
Decay MyD0
1.000      K-  pi+                PHSP;
Enddecay
CDecay Myanti-D0
#
Alias     MyD*-    D*-
Decay MyD*-
1.000      Myanti-D0 pi-          VSS;
Enddecay
#
#
############# Force excited states decay #############
#
Alias myD_1- D_1-
Decay myD_1-
0.6667    MyD*- pi0                        VVS_PWAVE  0.0 0.0 0.0 0.0 1.0 0.0;
Enddecay
#
Alias myD'_1- D'_1-
Decay myD'_1-
0.6667    MyD*- pi0                        VVS_PWAVE  1.0 0.0 0.0 0.0 0.0 0.0;
Enddecay
#
Alias myD_2*- D_2*-
Decay myD_2*-
0.2090    MyD*- pi0                        TVS_PWAVE  0.0 0.0 1.0 0.0 0.0 0.0;
Enddecay
#
#
#
Decay B0
# From decay table of EvtGen
# 0.0045   myD_1-   mu+  nu_mu       PHOTOS   ISGW2;
# 0.0040   myD'_1-   mu+  nu_mu      PHOTOS   ISGW2;
# 0.0010   myD_2*-   mu+  nu_mu      PHOTOS   ISGW2; # 0.0033*0.209/0.6667
# From PDG, including D** -> D* decay
0.0030   myD_1-   mu+  nu_mu       PHOTOS   ISGW2;
0.0027   myD'_1-   mu+  nu_mu      PHOTOS   ISGW2;
0.0010   myD_2*-   mu+  nu_mu      PHOTOS   ISGW2;
Enddecay
#
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
    MaxEta = cms.untracked.double(1.6),
    MinEta = cms.untracked.double(-1.6),
    MinPt = cms.untracked.double(6.7),
    ParticleID = cms.untracked.int32(13),
    MotherID = cms.untracked.int32(511)
)

DstFilter = cms.EDFilter(
    "PythiaDauVFilter",
    ParticleID         = cms.untracked.int32(-413),
    ChargeConjugation  = cms.untracked.bool(False),
    NumberDaughters    = cms.untracked.int32(2),
    DaughterIDs        = cms.untracked.vint32(-421, -211),
    MinPt              = cms.untracked.vdouble(0.5, 0.3),
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
